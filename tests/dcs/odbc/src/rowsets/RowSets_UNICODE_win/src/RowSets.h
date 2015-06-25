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

#ifndef ROWSETS_H
#define ROWSETS_H

#define ARGS                        _T("d:u:p:o:t:r:c:m:s:f:")
#ifndef FALSE
#define FALSE               0
#endif

#ifndef TRUE
#define TRUE                1
#endif

#define STRINGMAX                   256
//#define STRINGMAXDBL                41

// start ALM log changes
#define MAX_STRING_SIZE			500
// end ALM log changs

#define BIGENDIAN      0
#define LITTLEENDIAN   1

#define NO_ERROR_FND 1
#define ERROR_REPORT 2
#define IGNORE_ERROR 3
#define STOP -1

// modes
#define STANDARD       1
#define MODE_SPECIAL_1 2 // This mode is set by the system and can not be set by the application.

// features
#define HASH2 10
#define ASYNC 11

// operations
#define PREPARE_EXECUTE 20
#define EXECUTE_DIRECT  21

// actions
#define INSERT        30
#define SELECT        31
#define UPDATE        32
#define DELETE_PARAM  33
#define INSERT_BULK   34
#define INSERT_SELECT 35

// bindOrientation
#define ROW    40
#define COLUMN 41
#define SINGLE 42

// tableType
#define REGULAR         100
#define INDEX           101
#define POSOFF          102
#define MVS             103
#define RI              104
#define VOLATILE        105	
#define SURROGATE       106
#define SET             107
#define MULTISET        108
#define BEFORETRIGGER   109
#define AFTERTRIGGER    110

// injectionType
#define NO_ERRORS    60
#define DUPLICATEKEY 61
#define UNIQUECONST  62
#define SELECTIVE    63
#define NULLVALUE    64
#define DUPLICATEROW 65
#define CANCEL       67 
#define OVERFLOW     68
#define ERR_PER_ROW  69
#define ERR_PER_COL  70
#define FULL_ERRORS  71

// Application Name connection attribute
#define SQL_ATTR_ROLENAME			5002
// Max Application Name length
#define SQL_MAX_ROLENAME_LEN		128
//Driver side error
#define DRIVER_GOOD_BAD_MULCOL									72 //Some good rows, some errors, no warning, multiple columns
#define DRIVER_GOOD_WARNING_MULCOL								73 //Some good rows, no error, some warnings, multiple columns
#define DRIVER_GOOD_BAD_WARNING_MULCOL							74 //Some good rows, some errors, some warnings, multiple columns
#define DRIVER_ALL_BAD_MULCOL									75 //No good row, all errors, no warning, multiple columns
#define DRIVER_ALL_WARNING_MULCOL								76 //No good row, no error, all warnings, multiple columns
#define DRIVER_ALL_BAD_WARNING_MULCOL							77 //No good row, half errors and half warnings, multiple columns
//Server side error
#define SERVER_GOOD_BAD_MULCOL									78 //Some good rows, some bad rows, multiple columns (server error only with/without driver warning)
#define SERVER_ALL_BAD_MULCOL									79 //No good row, all errors, multiple columns (server error only with/without driver warning)
//Mix both driver and server
#define MIXED_DRIVERWARNING_SERVERBAD_GOOD_MULCOL				80 //Some driver warning, Some server error, some good, multiple columns
#define MIXED_DRIVERBAD_SERVERBAD_GOOD_MULCOL					81 //Some driver error, some server error, some good, multiple columns
#define MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_GOOD_MULCOL		82 //some driver error, driver warning, server error, good row, multiple columns
#define MIXED_DRIVERBAD_SERVERBAD_MULCOL						83 //driver errror, server error, no warning, multiple columns
#define MIXED_DRIVERWARNING_DRIVERBAD_SERVERBAD_MULCOL			84 //driver errror, server error, has warning, multiple columns

// Error messages to ignore.
#define NUMBER_OF_IGNORES 10

/*********************************************************************************/
//Define for bitflag types of violations
#define B_NOERRORS          1     //bit 0
#define B_DUPLICATEKEY      2     //bit 1
#define B_CHECKCONST        4     //bit 2
#define B_NULLVALUE         8     //bit 3
#define B_DUPLICATEROW      16    //bit 4
#define B_STRINGOVERFLOW    32    //bit 5
#define B_NUMERICOVERFLOW   64    //bit 6
#define B_SIGN2UNSIGN       128   //bit 7
#define B_DIVIDEDBYZERO     256   //bit 8
#define B_TIMESTAMP         512   //bit 9
/**********************************************************************************/

// The following contains the test information for each individual test.
struct _unitTest 
{
    int mode;
    int feature;
    int operation;
    int action;
    int bindOrientation;
    int tableType;
    int tableFeature;
    int injectionType;
    int numberOfRows;
    int rowsetSize;
    int commitRate;
} unitTest = { 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0 };

// This structure holds the column data based on row-wise binding.
typedef struct _table_rowset {
    SQLTCHAR             dt_char_utf8[STRINGMAX];           SQLLEN ptr_char_utf8;
    SQLTCHAR             dt_char_ucs[STRINGMAX];        SQLLEN ptr_char_ucs;
    SQLTCHAR             dt_varchar_utf8[STRINGMAX];        SQLLEN ptr_varchar_utf8;
    SQLTCHAR             dt_varchar_ucs[STRINGMAX];     SQLLEN ptr_varchar_ucs;
    SQLTCHAR             dt_longvarchar_utf8[STRINGMAX];    SQLLEN ptr_longvarchar_utf8;
    SQLTCHAR             dt_longvarchar_ucs[STRINGMAX]; SQLLEN ptr_longvarchar_ucs;            
    SQLTCHAR             dt_nchar[STRINGMAX];           SQLLEN ptr_nchar;
    SQLTCHAR             dt_ncharvarying[STRINGMAX];    SQLLEN ptr_ncharvarying;
    SQLTCHAR             dt_decimal_s[STRINGMAX];          SQLLEN ptr_decimal_s;
    SQLTCHAR             dt_decimal_u[STRINGMAX];          SQLLEN ptr_decimal_u;
    SQLTCHAR             dt_numeric_s[STRINGMAX];          SQLLEN ptr_numeric_s;
    SQLTCHAR             dt_numeric_u[STRINGMAX];          SQLLEN ptr_numeric_u;
    SQLTCHAR             dt_tinyint_s[STRINGMAX];          SQLLEN ptr_tinyint_s;
    SQLTCHAR             dt_tinyint_u[STRINGMAX];          SQLLEN ptr_tinyint_u;
    SQLTCHAR             dt_smallinteger_s[STRINGMAX];     SQLLEN ptr_smallinteger_s;
    SQLTCHAR             dt_smallinteger_u[STRINGMAX];     SQLLEN ptr_smallinteger_u;
    SQLTCHAR             dt_integer_s[STRINGMAX];          SQLLEN ptr_integer_s;
    SQLTCHAR             dt_integer_u[STRINGMAX];          SQLLEN ptr_integer_u;            
    SQLTCHAR             dt_largeint[STRINGMAX];           SQLLEN ptr_largeint;
    SQLTCHAR             dt_real[STRINGMAX];               SQLLEN ptr_real;
    SQLTCHAR             dt_float[STRINGMAX];              SQLLEN ptr_float;
    SQLTCHAR             dt_double_precision[STRINGMAX];   SQLLEN ptr_double_precision;
    DATE_STRUCT         dt_date;                          SQLLEN ptr_date;
    TIME_STRUCT         dt_time;                          SQLLEN ptr_time;
    TIMESTAMP_STRUCT    dt_timestamp;                     SQLLEN ptr_timestamp;
    SQL_INTERVAL_STRUCT dt_interval_year;                 SQLLEN ptr_interval_year;
    SQL_INTERVAL_STRUCT dt_interval_month;                SQLLEN ptr_interval_month;
    SQL_INTERVAL_STRUCT dt_interval_day;                  SQLLEN ptr_interval_day;
    SQL_INTERVAL_STRUCT dt_interval_hour;                 SQLLEN ptr_interval_hour;
    SQL_INTERVAL_STRUCT dt_interval_minute;               SQLLEN ptr_interval_minute;
    SQL_INTERVAL_STRUCT dt_interval_second;               SQLLEN ptr_interval_second;
    SQL_INTERVAL_STRUCT dt_interval_year_to_month;        SQLLEN ptr_interval_year_to_month;
    SQL_INTERVAL_STRUCT dt_interval_day_to_hour;          SQLLEN ptr_interval_day_to_hour;
    SQL_INTERVAL_STRUCT dt_interval_day_to_minute;        SQLLEN ptr_interval_day_to_minute;
    SQL_INTERVAL_STRUCT dt_interval_day_to_second;        SQLLEN ptr_interval_day_to_second;
    SQL_INTERVAL_STRUCT dt_interval_hour_to_minute;       SQLLEN ptr_interval_hour_to_minute;
    SQL_INTERVAL_STRUCT dt_interval_hour_to_second;       SQLLEN ptr_interval_hour_to_second;
    SQL_INTERVAL_STRUCT dt_interval_minute_to_second;     SQLLEN ptr_interval_minute_to_second;
    SQLTCHAR             dt_bignum_s[STRINGMAX];           SQLLEN ptr_bignum_s;
    SQLTCHAR             dt_bignum_u[STRINGMAX];           SQLLEN ptr_bignum_u;
} table_rowset;

// These variables are simular to the fields in the above structure but are used
// for column-wise binding.
SQLTCHAR             *dt_char_utf8;                   SQLLEN *ptr_char_utf8;
SQLTCHAR             *dt_char_ucs;                   SQLLEN *ptr_char_ucs;
SQLTCHAR             *dt_varchar_utf8;                SQLLEN *ptr_varchar_utf8;
SQLTCHAR             *dt_varchar_ucs;                SQLLEN *ptr_varchar_ucs;
SQLTCHAR             *dt_longvarchar_utf8;            SQLLEN *ptr_longvarchar_utf8;
SQLTCHAR             *dt_longvarchar_ucs;            SQLLEN *ptr_longvarchar_ucs;            
SQLTCHAR             *dt_nchar;                      SQLLEN *ptr_nchar;
SQLTCHAR             *dt_ncharvarying;               SQLLEN *ptr_ncharvarying;
SQLTCHAR             *dt_decimal_s;                  SQLLEN *ptr_decimal_s;
SQLTCHAR             *dt_decimal_u;                  SQLLEN *ptr_decimal_u;
SQLTCHAR             *dt_numeric_s;                  SQLLEN *ptr_numeric_s;
SQLTCHAR             *dt_numeric_u;                  SQLLEN *ptr_numeric_u;
SQLTCHAR             *dt_tinyint_s;                  SQLLEN *ptr_tinyint_s;
SQLTCHAR             *dt_tinyint_u;                  SQLLEN *ptr_tinyint_u;
SQLTCHAR             *dt_smallinteger_s;             SQLLEN *ptr_smallinteger_s;
SQLTCHAR             *dt_smallinteger_u;             SQLLEN *ptr_smallinteger_u;
SQLTCHAR             *dt_integer_s;                  SQLLEN *ptr_integer_s;
SQLTCHAR             *dt_integer_u;                  SQLLEN *ptr_integer_u;            
SQLTCHAR             *dt_largeint;                   SQLLEN *ptr_largeint;
SQLTCHAR             *dt_real;                       SQLLEN *ptr_real;
SQLTCHAR             *dt_float;                      SQLLEN *ptr_float;
SQLTCHAR             *dt_double_precision;           SQLLEN *ptr_double_precision;
DATE_STRUCT         *dt_date;                       SQLLEN *ptr_date;
TIME_STRUCT         *dt_time;                       SQLLEN *ptr_time;
TIMESTAMP_STRUCT    *dt_timestamp;                  SQLLEN *ptr_timestamp;
SQL_INTERVAL_STRUCT *dt_interval_year;              SQLLEN *ptr_interval_year;
SQL_INTERVAL_STRUCT *dt_interval_month;             SQLLEN *ptr_interval_month;
SQL_INTERVAL_STRUCT *dt_interval_day;               SQLLEN *ptr_interval_day;
SQL_INTERVAL_STRUCT *dt_interval_hour;              SQLLEN *ptr_interval_hour;
SQL_INTERVAL_STRUCT *dt_interval_minute;            SQLLEN *ptr_interval_minute;
SQL_INTERVAL_STRUCT *dt_interval_second;            SQLLEN *ptr_interval_second;
SQL_INTERVAL_STRUCT *dt_interval_year_to_month;     SQLLEN *ptr_interval_year_to_month;
SQL_INTERVAL_STRUCT *dt_interval_day_to_hour;       SQLLEN *ptr_interval_day_to_hour;
SQL_INTERVAL_STRUCT *dt_interval_day_to_minute;     SQLLEN *ptr_interval_day_to_minute;
SQL_INTERVAL_STRUCT *dt_interval_day_to_second;     SQLLEN *ptr_interval_day_to_second;
SQL_INTERVAL_STRUCT *dt_interval_hour_to_minute;    SQLLEN *ptr_interval_hour_to_minute;
SQL_INTERVAL_STRUCT *dt_interval_hour_to_second;    SQLLEN *ptr_interval_hour_to_second;
SQL_INTERVAL_STRUCT *dt_interval_minute_to_second;  SQLLEN *ptr_interval_minute_to_second;
SQLTCHAR             *dt_bignum_s;                   SQLLEN *ptr_bignum_s;
SQLTCHAR             *dt_bignum_u;                   SQLLEN *ptr_bignum_u;

// This structure holds the data for charset.
typedef struct var_list_tt {
	int last;
	TCHAR *var_name;
	TCHAR *value;
} var_list_t;

// Global Variables.
SQLHANDLE  handle[ 5 ];     // 0 = nothing, 1 = environment 2 = connection 3 = statement 4 = used for DELETE and UPDATE
TCHAR      *datasource;     // Datasource name to make the ODBC connection through.
TCHAR      *uid;            // User identification to run the tests as.
TCHAR      *password;       // User identification password.
TCHAR		*charset;       //Charset
TCHAR      *machine = (TCHAR*)"local";
TCHAR      *secondaryRole = (TCHAR*)"--";
bool      debug = false;    // Print out debug info
int       errorChecking = STANDARD;   // Error checking type.
int       failureInjectionCount;
int       goodRowCount;
TCHAR	  dataCQD[ 512 ];		//This is for CQD checking
TCHAR* String_OverFlow;

// Post rowset execution analysis. This allows us to check the statuses of the rows we inserted.
SQLUSMALLINT *rowsetStatusArray; // Array showing the status of each row after running SQLExecute().
SQLUSMALLINT *expectedRowsetStatusArray; // Expected Array showing the status of each row after running SQLExecute().
SQLUSMALLINT *rowsetOperationArray; // Array showing which rows to process when running SQLExecute().
SQLULEN       rowsProcessed;     // The number of rows processed after running SQLExecute().
table_rowset *rowset;  // Where we will store the data prior to inserting it into the database.

// Timing metrics
bool  timeMetrics = false; // Display time metrics information. 
TCHAR logfilename[256];

// SK - for ALM log
/****************************************************************
** Local variables for ALM
****************************************************************/
time_t	ALM_Test_start, ALM_Test_end;
TCHAR		ALM_log_file_buff[1024];
TCHAR		Heading[MAX_STRING_SIZE];
TCHAR		ALM_NextTestInfo[MAX_STRING_SIZE];
TCHAR		ALM_TestCaseId[12];   
typedef enum PassFail {PASSED, FAILED} PassFail;
PassFail _TestCase;
// End for ALM log

// Function Definitions.
/* For ALM Formatted Log output */
void ALM_LogTestCaseInfo(TCHAR *, TCHAR *, int, int);
void ALM_LogTestResultInfo(PassFail, time_t, time_t);
void ALM_TestInformation(TCHAR *);
/* End  For ALM Formatted Log output */

// Function Definitions.
bool NextTest( void );
bool IgnoreTest( void );
bool EstablishHandlesAndConnection( void );
bool CreateTable( void );
void IgnoreMsg( SQLTCHAR *state, SDWORD nativeError );
bool ShouldIgnoreMsg( SQLTCHAR *state, SDWORD nativeError );
void ClearIgnore( void );
int  CheckMsgs( TCHAR* sqlFunction, int lineNumber );
void DeleteHandles( void );
bool FreeHandles( void );
bool CleanupMisc( void );
bool DeleteRows( void );
bool DropTable( void );
void PrintTestInformation( void );
void FreeRowsets( int bindOrientations );
void AllocateRowsets( int bindOrientations, int rowsetSizes );
bool BindParameters( void );
void AssignRow( int rowsetPos, int column1Value, int column2Value );
bool RowsetDML( void );
bool RowsetDMLBulk( void );
bool BindCols( void );
bool CompareRow( int rowsetPos, int iteration );
bool RowsetFetch( void );
bool RowsetDelete_FromCursorPosition( int errorMatrixPos );
TCHAR* Param_Status_Ptr( SQLUSMALLINT parameter_status );
void DisplayTimeMetrics( void );
void RecordToLog( TCHAR* format, ... );
TCHAR* CheckForCQD( TCHAR *CQD );
int TestByteOrder(void);
bool BindParametersA( int bindOrientations, int actions, int injectionTypes );

/*For Character Set*/
int next_line(TCHAR *lineOut, FILE *scriptFD);
var_list_t* load_api_vars(TCHAR *api, TCHAR *textFile);
void print_list (var_list_t *var_list);
void free_list (var_list_t *var_list);
TCHAR* var_mapping(TCHAR *var_name, var_list_t *var_list);

/* SQ */ extern int injectionTypes[];

int TestByteOrder(void)
{
    short int word = 0x0001;
    TCHAR *byte = (TCHAR *) &word;
    return(byte[0] ? LITTLEENDIAN : BIGENDIAN);
}

TCHAR * __itoa(int n, TCHAR *buff, int base) {

   TCHAR t[100], *c=t, *f=buff;
   int d;
   int bit;

   if (base == 10) {
     if (n < 0) {
        *(f++) = '-';
        n = -n;
     }

   while ( n > 0) {
      d = n % base;
      *(c++) = d + '0';
      n = n / base;
   }
   
   }
   
   else {
	  if (base == 2) bit = 1;
      else if (base == 8) bit = 3;
      else if (base == 16) bit = 4;
      else printf("Base value unknown!\n");

	  while (n != 0) {
		 d = (n  & (base-1));
		 *(c++) = d < 10 ? d + '0' : d - 10 + 'A';
		 n = (unsigned int) n >> bit;
	  }

   }

   c--;

   while (c >= t) *(f++) = *(c--);
     
   *f = '\0';
   return buff;
}

int int_to_ucs2 (int intVal, TCHAR *usc2_array) {
	int i=0, j=0;
	TCHAR buffer[STRINGMAX];

	__itoa (intVal,buffer,10);
	for (i=0; i<(int)_tcslen(buffer); i++) {
		if (TestByteOrder() == LITTLEENDIAN) {
			usc2_array[j++] = buffer[i];
			usc2_array[j++] = '\0';
		}
		else {
			usc2_array[j++] = '\0';
			usc2_array[j++] = buffer[i];
		}
	}

	usc2_array[j++] = '\0';	
	usc2_array[j++] = '\0';

	return j;
}

bool array_cmp(TCHAR *arr1, TCHAR *arr2, int size) {
	for (int i=0; i<size; i++) {
		if (arr1[i] != arr2[i]) return 1;
	}

	return 0;
}

/* Function          : Param_Status_Str
   Calling Arguments : int : The parameter status definition
   Return Arguments  : TCHAR* : The C string representing the parameter status

   Description: 
   This returns the parameter status definition C string.
*/

TCHAR* Param_Status_Ptr( SQLUSMALLINT parameter_status )
{
    switch( parameter_status )
    {
        case SQL_PARAM_SUCCESS:
            return( _T("SQL_PARAM_SUCCESS") );
        case SQL_PARAM_SUCCESS_WITH_INFO:
             return( _T("SQL_PARAM_SUCCESS_WITH_INFO") );
        case SQL_PARAM_ERROR:
             return( _T("SQL_PARAM_ERROR") );
        case SQL_PARAM_UNUSED:
             return( _T("SQL_PARAM_UNUSED") );
        case SQL_PARAM_DIAG_UNAVAILABLE:
             return( _T("SQL_PARAM_DIAG_UNAVAILABLE") );
        default:
            return( _T("UNKNOWN") );
    }
    return( _T("INTERNAL ERROR: Param_Status_Ptr( )") );
}

/* Function          : DisplayTimeMetrics
   Calling Arguments : None
   Return Arguments  : None

   Description: 
   Displays time metrics for tests run.
*/

void DisplayTimeMetrics( void )
{
    /*****
    int testLoop = 0;
    long total_time;
    long total_tests;
   
   total_time = 0;
   total_tests = 0;
    while( testMatrix[ testLoop ].action != STOP )
    {
        if( ( testMatrix[ testLoop ].returnCode == true ) && 
            ( testMatrix[ testLoop ].action == INSERT ) && 
            ( testMatrix[ testLoop ].bindOrientation == ROW ) )
        {
            total_time += testMatrix[ testLoop ].runningTime;
            total_tests++;
        }
        testLoop++;
    }
    RecordToLog(" Average row-wise insert time in seconds: %ld\n", ( total_time / total_tests ) );
    return;
*****/    
}

/* Method            : RecordToLog
   Calling Arguments : TCHAR* : vfwRecordToLog() format string.
                       ...   : arguments for formated string.
   Return Arguments  : void

   Description: 
   Writes the message to a log file.
*/

void RecordToLog( TCHAR* format, ... )
{
    FILE *logFilePtr;
    //time_t wall_clock;
    //TCHAR date[ 100 ];
	errno_t err;
	int ret;

	// Opens for writing at the end of the file (appending) without removing 
	// the EOF marker before writing new data to the file; 
	// creates the file first if it doesn't exist.
	if( (err  = _wfopen_s( &logFilePtr, logfilename, _T("a") )) !=0 )
		RecordToLog( _T("The log file was not opened for appending\n") );

    if( logFilePtr == NULL ) 
    {
        // TODO: Debugging
    }

    va_list ArgumentList;
    if( logFilePtr != (FILE*)NULL )
    {
		//if (debug) {
		//	wall_clock = time( NULL );
		//	_tcsftime( date, 100, _T("%Y %b %d %H:%M:%S"), localtime( &wall_clock ) );
		//	if( _ftprintf( logFilePtr, _T("[%s] "), date ) == -1 )
		//	{
		//		// TODO: Debugging
		//	}
		//}

        va_start( ArgumentList, format );
        _vtprintf( format, ArgumentList );
		va_end(ArgumentList);

        va_start( ArgumentList, format );
        ret = _vftprintf( logFilePtr, format, ArgumentList );
        va_end(ArgumentList);

        if( ret == -1 )
        {
            // TODO: Debugging
        }
        if( fflush( logFilePtr ) == EOF )
        {
            // TODO: Debugging
        }

		if( fclose( logFilePtr ) == EOF )
		{
			// TODO: Debugging.
		}
	}
    return;
}

/* Method            : RecordTo_ALM_Log
   Calling Arguments : TCHAR* : vfwRecordToLog() format string.
                       ...   : arguments for formated string.
   Return Arguments  : void

   Description: 
   Writes the message to the ALM log file with ALM format.
*/
void RecordTo_ALM_Log( TCHAR* format, ... )
{
    FILE *ALM_logFilePtr;
	tm newtime;
    time_t wall_clock;
    TCHAR date[ 100 ];
	int ret;
	errno_t err;




	if( (err  = _wfopen_s( &ALM_logFilePtr, ALM_log_file_buff, _T("a+") )) !=0 )
		RecordToLog( _T("The ALM log file was not opened for appending\n") );

	if( ALM_logFilePtr == NULL ) 
    {
        // TODO: Debugging
    }

    va_list ArgumentList;
    if( ALM_logFilePtr != (FILE*)NULL )
    {
		if (debug) {
			// Get time as 64-bit integer.
			_time64( &wall_clock ); 
			// Convert to local time.
			err = _localtime64_s( &newtime, &wall_clock ); 
			if (err)
			{
				printf("Invalid argument to _localtime64_s.");
				exit(1);
			}


			wall_clock = time( NULL );
			wcsftime( date, 100, _T("%Y %b %d %H:%M:%S"), &newtime );
			if( _ftprintf( ALM_logFilePtr, _T("[%s] "), date ) == -1 )
			{
				// TODO: Debugging
			}
		}

//      va_start( ArgumentList, format );
//      vprintf( format, ArgumentList );
//      va_end(ArgumentList);

        va_start( ArgumentList, format );
        ret = vfwprintf( ALM_logFilePtr, format, ArgumentList );
        va_end(ArgumentList);

        if( ret == -1 )
        {
            // TODO: Debugging
        }
        if( fflush( ALM_logFilePtr ) == EOF )
        {
            // TODO: Debugging
        }

		if( fclose( ALM_logFilePtr ) == EOF )
		{
			// TODO: Debugging.
		}
	}
    return;
}


/* Method            : CheckForCQD
   Calling Arguments : TCHAR* : CQD that is being looked for.
   Return Arguments  : TCHAR* : CQD value. An empty string is returned if 
                               nothing is retrieved.

   Description: 
   This looks for a CQD and thn returns the CQD value.
*/
TCHAR* CheckForCQD( TCHAR *CQD )
{
    SQLRETURN  retcode;       // Used to gather the return value of all ODBC API calls.
    // We need to check _ALL_ CQD's on the system. So we make sure we can see the ones not
    // exposed to the customer too.
    while( (retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)_T("CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'ON' "), SQL_NTS ) ) == SQL_STILL_EXECUTING );
    if( retcode != SQL_SUCCESS )
    {
        CheckMsgs( _T("SQLExecDirect()"), __LINE__ );
        retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( _T("SQLFreeStmt()"), __LINE__ );
        }
	    while( (retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)_T("CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'OFF' "), SQL_NTS ) ) == SQL_STILL_EXECUTING );
        return _T(" ") ;
    }

    // Execute the command to request information about the CQD.
    TCHAR *SQLCommand;
    SQLCommand = (TCHAR *)malloc( (_tcslen( CQD ) + 50) * sizeof(TCHAR) );
    swprintf( SQLCommand, _tcslen( SQLCommand ), _T("SHOWCONTROL DEFAULT %s, MATCH FULL, NO HEADER"), CQD );
    while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)SQLCommand, SQL_NTS ) ) == SQL_STILL_EXECUTING );
    free( SQLCommand );
    if( retcode != SQL_SUCCESS )
    {
        CheckMsgs( _T("SQLExecDirect()"), __LINE__ );
        retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( _T("SQLFreeStmt()"), __LINE__ );
        }
	    while( (retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)_T("CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'OFF' "), SQL_NTS ) ) == SQL_STILL_EXECUTING );
        return _T(" ") ;
    }

    // Now we fetch the data if there is any.
    SQLLEN dataPtr;
    dataPtr = SQL_NTS;
    retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 1, SQL_C_TCHAR, (SQLPOINTER) dataCQD, 512*sizeof(TCHAR), &dataPtr );
    if( retcode != SQL_SUCCESS )
    {
        CheckMsgs( _T("SQLBindCol()"), __LINE__ );
        retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( _T("SQLFreeStmt()"), __LINE__ );
        }
	    while( (retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)_T("CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'OFF' "), SQL_NTS ) ) == SQL_STILL_EXECUTING );
        return _T(" ") ;
    }

	while( ( retcode = SQLFetch( handle[ SQL_HANDLE_STMT ] ) ) == SQL_STILL_EXECUTING );
	if( retcode == SQL_SUCCESS || retcode == SQL_SUCCESS_WITH_INFO )
    {
		retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
		if( retcode != SQL_SUCCESS )    
		{
			CheckMsgs( _T("SQLFreeStmt()"), __LINE__ );
		}
		while( (retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)_T("CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'OFF' "), SQL_NTS ) ) == SQL_STILL_EXECUTING );
		return dataCQD;
    }

    retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( _T("SQLFreeStmt()"), __LINE__ );
    }
	while( (retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLTCHAR*)_T("CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'OFF' "), SQL_NTS ) ) == SQL_STILL_EXECUTING );
    return _T(" ");
}

void DisplayRowsets(int bindOrientations, int rowsetPos) {
    switch( bindOrientations )
    {
        case ROW:
        case SINGLE:
		if (rowset[ rowsetPos ].dt_integer_s[0] != '\0')
			RecordToLog( _T("[%s] %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %d %s %s\n"), 
				(TCHAR*)rowset[ rowsetPos ].dt_largeint,
				(TCHAR*)rowset[ rowsetPos ].dt_char_utf8,
				(TCHAR*)rowset[ rowsetPos ].dt_char_ucs,
				(TCHAR*)rowset[ rowsetPos ].dt_varchar_utf8,
				(TCHAR*)rowset[ rowsetPos ].dt_varchar_ucs,
				(TCHAR*)rowset[ rowsetPos ].dt_longvarchar_utf8,
				(TCHAR*)rowset[ rowsetPos ].dt_longvarchar_ucs,
				(TCHAR*)rowset[ rowsetPos ].dt_nchar,
				(TCHAR*)rowset[ rowsetPos ].dt_ncharvarying,
				(TCHAR*)rowset[ rowsetPos ].dt_decimal_s,
				(TCHAR*)rowset[ rowsetPos ].dt_decimal_u,
				(TCHAR*)rowset[ rowsetPos ].dt_numeric_s,
				(TCHAR*)rowset[ rowsetPos ].dt_numeric_u,
				(TCHAR*)rowset[ rowsetPos ].dt_tinyint_s,
				(TCHAR*)rowset[ rowsetPos ].dt_tinyint_u,
				(TCHAR*)rowset[ rowsetPos ].dt_smallinteger_s,
				(TCHAR*)rowset[ rowsetPos ].dt_smallinteger_u,
 				(TCHAR*)rowset[ rowsetPos ].dt_integer_s,
				(TCHAR*)rowset[ rowsetPos ].dt_integer_u,
				(TCHAR*)rowset[ rowsetPos ].dt_real,
				(TCHAR*)rowset[ rowsetPos ].dt_float,
				(TCHAR*)rowset[ rowsetPos ].dt_double_precision,
				rowset[ rowsetPos ].dt_timestamp.day,
				(TCHAR*)rowset[ rowsetPos ].dt_bignum_s,
				(TCHAR*)rowset[ rowsetPos ].dt_bignum_u
			);
		else
			RecordToLog( _T("[%s] %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s null %s %s %s %s %s %d %s %s\n"), 
				(TCHAR*)rowset[ rowsetPos ].dt_largeint,
				(TCHAR*)rowset[ rowsetPos ].dt_char_utf8,
				(TCHAR*)rowset[ rowsetPos ].dt_char_ucs,
				(TCHAR*)rowset[ rowsetPos ].dt_varchar_utf8,
				(TCHAR*)rowset[ rowsetPos ].dt_varchar_ucs,
				(TCHAR*)rowset[ rowsetPos ].dt_longvarchar_utf8,
				(TCHAR*)rowset[ rowsetPos ].dt_longvarchar_ucs,
				(TCHAR*)rowset[ rowsetPos ].dt_nchar,
				(TCHAR*)rowset[ rowsetPos ].dt_ncharvarying,
				(TCHAR*)rowset[ rowsetPos ].dt_decimal_s,
				(TCHAR*)rowset[ rowsetPos ].dt_decimal_u,
				(TCHAR*)rowset[ rowsetPos ].dt_numeric_s,
				(TCHAR*)rowset[ rowsetPos ].dt_numeric_u,
				(TCHAR*)rowset[ rowsetPos ].dt_tinyint_s,
				(TCHAR*)rowset[ rowsetPos ].dt_tinyint_u,
				(TCHAR*)rowset[ rowsetPos ].dt_smallinteger_s,
				(TCHAR*)rowset[ rowsetPos ].dt_smallinteger_u,
 				//(TCHAR*)rowset[ rowsetPos ].dt_integer_s,
				(TCHAR*)rowset[ rowsetPos ].dt_integer_u,
				(TCHAR*)rowset[ rowsetPos ].dt_real,
				(TCHAR*)rowset[ rowsetPos ].dt_float,
				(TCHAR*)rowset[ rowsetPos ].dt_double_precision,
				rowset[ rowsetPos ].dt_timestamp.day,
				(TCHAR*)rowset[ rowsetPos ].dt_bignum_s,
				(TCHAR*)rowset[ rowsetPos ].dt_bignum_u
			);
            break;
        case COLUMN:
		if (dt_integer_s[ rowsetPos * STRINGMAX  ] != '\0')
			RecordToLog( _T("[%s] %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %d %s %s\n"), 
            			(TCHAR*)&dt_largeint[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_char_utf8[ rowsetPos * STRINGMAX ],
            			(TCHAR*)&dt_char_ucs[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_varchar_utf8[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_varchar_ucs[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_longvarchar_utf8[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_longvarchar_ucs[ rowsetPos * STRINGMAX  ],            
            			(TCHAR*)&dt_nchar[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_ncharvarying[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_decimal_s[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_decimal_u[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_numeric_s[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_numeric_u[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_tinyint_s[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_tinyint_u[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_smallinteger_s[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_smallinteger_u[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_integer_s[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_integer_u[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_real[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_float[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_double_precision[ rowsetPos * STRINGMAX  ],
						dt_timestamp[ rowsetPos ].day,
            			(TCHAR*)&dt_bignum_s[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_bignum_u[ rowsetPos * STRINGMAX  ]
			);
		else
			RecordToLog( _T("[%s] %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s null %s %s %s %s %s %d %s %s\n"), 
            			(TCHAR*)&dt_largeint[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_char_utf8[ rowsetPos * STRINGMAX ],
            			(TCHAR*)&dt_char_ucs[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_varchar_utf8[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_varchar_ucs[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_longvarchar_utf8[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_longvarchar_ucs[ rowsetPos * STRINGMAX  ],            
            			(TCHAR*)&dt_nchar[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_ncharvarying[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_decimal_s[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_decimal_u[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_numeric_s[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_numeric_u[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_tinyint_s[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_tinyint_u[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_smallinteger_s[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_smallinteger_u[ rowsetPos * STRINGMAX  ],
            			//(TCHAR*)&dt_integer_s[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_integer_u[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_real[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_float[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_double_precision[ rowsetPos * STRINGMAX  ],
                        dt_timestamp[ rowsetPos ].day,
            			(TCHAR*)&dt_bignum_s[ rowsetPos * STRINGMAX  ],
            			(TCHAR*)&dt_bignum_u[ rowsetPos * STRINGMAX  ]
			);
			break;
	}
}

/* Function          : Allocate rowsets.
   Calling Arguments : int : The test dictates the type of binding orientation that is to be used.
   Return Arguments  : none

   Description: 
   This allocates the row-wise and column-wise data structures.
 */
 
 void AllocateRowsets( int bindOrientations, int rowsetSizes )
 {
    switch( bindOrientations )
    {
        case ROW:
        case SINGLE: // <---Got to love row-wise rowsets!
            if( rowsetSizes > 0 )
            {
                rowset = (table_rowset *)malloc( rowsetSizes * sizeof( table_rowset ) );
                memset( rowset, 0, rowsetSizes * sizeof( table_rowset ) );
            }
            else
            {
                rowset = (table_rowset *)malloc( 1 * sizeof( table_rowset ) );
                memset(rowset, 0, sizeof( table_rowset ) );
            }
            break;
        case COLUMN:
            if( rowsetSizes > 0 )
            {
                dt_char_utf8 = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_char_utf8 = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_char_ucs = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_char_ucs = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_varchar_utf8 = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_varchar_utf8 = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_varchar_ucs = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_varchar_ucs = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_longvarchar_utf8 = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_longvarchar_utf8 = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_longvarchar_ucs = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_longvarchar_ucs = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_nchar = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_nchar = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_ncharvarying = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_ncharvarying = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_decimal_s = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_decimal_s = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_decimal_u = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_decimal_u = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_numeric_s = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_numeric_s = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_numeric_u = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_numeric_u = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_tinyint_s = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_tinyint_s = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_tinyint_u = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_tinyint_u = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_smallinteger_s = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_smallinteger_s = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_smallinteger_u = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_smallinteger_u = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_integer_s = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_integer_s = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_integer_u = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_integer_u = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_largeint = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_largeint = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_real = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR) );
                ptr_real = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_float = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR) );
                ptr_float = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_double_precision = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR) );
                ptr_double_precision = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_date = (DATE_STRUCT*) malloc( rowsetSizes * sizeof( DATE_STRUCT ) );
                ptr_date = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_time = (TIME_STRUCT*) malloc( rowsetSizes * sizeof( TIME_STRUCT ) );
                ptr_time = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_timestamp = (TIMESTAMP_STRUCT*) malloc( rowsetSizes * sizeof( TIMESTAMP_STRUCT ) );
                ptr_timestamp = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_interval_year = (SQL_INTERVAL_STRUCT*) malloc( rowsetSizes * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_year = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_interval_month = (SQL_INTERVAL_STRUCT*) malloc( rowsetSizes * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_month = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_interval_day = (SQL_INTERVAL_STRUCT*) malloc( rowsetSizes * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_day = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_interval_hour = (SQL_INTERVAL_STRUCT*) malloc( rowsetSizes * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_hour = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_interval_minute = (SQL_INTERVAL_STRUCT*) malloc( rowsetSizes * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_minute = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_interval_second = (SQL_INTERVAL_STRUCT*) malloc( rowsetSizes * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_second = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_interval_year_to_month = (SQL_INTERVAL_STRUCT*) malloc( rowsetSizes * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_year_to_month = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_interval_day_to_hour = (SQL_INTERVAL_STRUCT*) malloc( rowsetSizes * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_day_to_hour = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_interval_day_to_minute = (SQL_INTERVAL_STRUCT*) malloc( rowsetSizes * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_day_to_minute = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_interval_day_to_second = (SQL_INTERVAL_STRUCT*) malloc( rowsetSizes * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_day_to_second = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_interval_hour_to_minute = (SQL_INTERVAL_STRUCT*) malloc( rowsetSizes * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_hour_to_minute = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_interval_hour_to_second = (SQL_INTERVAL_STRUCT*) malloc( rowsetSizes * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_hour_to_second = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_interval_minute_to_second = (SQL_INTERVAL_STRUCT*) malloc( rowsetSizes * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_minute_to_second = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_bignum_s = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_bignum_s = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_bignum_u = (SQLTCHAR *) malloc( rowsetSizes * STRINGMAX * sizeof(TCHAR));
                ptr_bignum_u = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );

				memset(dt_char_utf8 , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_char_utf8 , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_char_ucs , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_char_ucs , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_varchar_utf8 , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_varchar_utf8 , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_varchar_ucs , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_varchar_ucs , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_longvarchar_utf8 , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_longvarchar_utf8 , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_longvarchar_ucs , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_longvarchar_ucs , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_nchar , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_nchar , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_ncharvarying , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_ncharvarying , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_decimal_s , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_decimal_s , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_decimal_u ,0,  rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_decimal_u , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_numeric_s , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_numeric_s , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_numeric_u , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_numeric_u , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_tinyint_s , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_tinyint_s , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_tinyint_u , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_tinyint_u , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_smallinteger_s , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_smallinteger_s , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_smallinteger_u , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_smallinteger_u , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_integer_s , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_integer_s , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_integer_u , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_integer_u , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_largeint , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_largeint , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_real , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_real , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_float , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_float , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_double_precision , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_double_precision , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_date , 0, rowsetSizes *   sizeof( DATE_STRUCT ) );
                memset(ptr_date , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_time , 0, rowsetSizes *   sizeof( TIME_STRUCT ) );
                memset(ptr_time , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_timestamp , 0, rowsetSizes *   sizeof( TIMESTAMP_STRUCT ) );
                memset(ptr_timestamp , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_interval_year ,0,  rowsetSizes *   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_year , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_interval_month , 0, rowsetSizes *   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_month , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_interval_day , 0, rowsetSizes *   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_day , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_interval_hour , 0, rowsetSizes *   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_hour , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_interval_minute , 0, rowsetSizes *   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_minute , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_interval_second , 0, rowsetSizes *   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_second , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_interval_year_to_month , 0, rowsetSizes *   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_year_to_month , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_interval_day_to_hour , 0, rowsetSizes *   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_day_to_hour , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_interval_day_to_minute , 0, rowsetSizes *   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_day_to_minute , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_interval_day_to_second , 0, rowsetSizes *   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_day_to_second , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_interval_hour_to_minute , 0, rowsetSizes *   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_hour_to_minute , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_interval_hour_to_second , 0, rowsetSizes *   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_hour_to_second , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_interval_minute_to_second , 0, rowsetSizes *   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_minute_to_second ,0,  rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_bignum_s , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_bignum_s , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_bignum_u , 0, rowsetSizes * STRINGMAX * sizeof(TCHAR));
                memset(ptr_bignum_u , 0, rowsetSizes *   sizeof( SQLLEN ) );
			}
            else
            {
                dt_char_utf8 = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR));
                ptr_char_utf8 = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_char_ucs = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR));
                ptr_char_ucs = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_varchar_utf8 = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR));
                ptr_varchar_utf8 = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_varchar_ucs = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR));
                ptr_varchar_ucs = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_longvarchar_utf8 = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR));
                ptr_longvarchar_utf8 = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_longvarchar_ucs = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR));
                ptr_longvarchar_ucs = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_nchar = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR) );
                ptr_nchar = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_ncharvarying = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR) );
                ptr_ncharvarying = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_decimal_s = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR));
                ptr_decimal_s = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_decimal_u = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR));
                ptr_decimal_u = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_numeric_s = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR));
                ptr_numeric_s = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_numeric_u = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR));
                ptr_numeric_u = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_tinyint_s = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR) );
                ptr_tinyint_s = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_tinyint_u = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR) );
                ptr_tinyint_u = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_smallinteger_s = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR) );
                ptr_smallinteger_s = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_smallinteger_u = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR) );
                ptr_smallinteger_u = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_integer_s = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR) );
                ptr_integer_s = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_integer_u = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR) );
                ptr_integer_u = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_largeint = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR) );
                ptr_largeint = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_real = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR) );
                ptr_real = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_float = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR) );
                ptr_float = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_double_precision = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR) );
                ptr_double_precision = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_date = (DATE_STRUCT*) malloc( 1 * sizeof( DATE_STRUCT ) );
                ptr_date = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_time = (TIME_STRUCT*) malloc( 1 * sizeof( TIME_STRUCT ) );
                ptr_time = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_timestamp = (TIMESTAMP_STRUCT*) malloc( 1 * sizeof( TIMESTAMP_STRUCT ) );
                ptr_timestamp = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_interval_year = (SQL_INTERVAL_STRUCT*) malloc( 1 * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_year = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_interval_month = (SQL_INTERVAL_STRUCT*) malloc( 1 * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_month = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_interval_day = (SQL_INTERVAL_STRUCT*) malloc( 1 * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_day = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_interval_hour = (SQL_INTERVAL_STRUCT*) malloc( 1 * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_hour = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_interval_minute = (SQL_INTERVAL_STRUCT*) malloc( 1 * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_minute = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_interval_second = (SQL_INTERVAL_STRUCT*) malloc( 1 * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_second = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_interval_year_to_month = (SQL_INTERVAL_STRUCT*) malloc( 1 * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_year_to_month = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_interval_day_to_hour = (SQL_INTERVAL_STRUCT*) malloc( 1 * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_day_to_hour = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_interval_day_to_minute = (SQL_INTERVAL_STRUCT*) malloc( 1 * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_day_to_minute = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_interval_day_to_second = (SQL_INTERVAL_STRUCT*) malloc( 1 * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_day_to_second = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_interval_hour_to_minute = (SQL_INTERVAL_STRUCT*) malloc( 1 * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_hour_to_minute = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_interval_hour_to_second = (SQL_INTERVAL_STRUCT*) malloc( 1 * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_hour_to_second = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_interval_minute_to_second = (SQL_INTERVAL_STRUCT*) malloc( 1 * sizeof( SQL_INTERVAL_STRUCT ) );
                ptr_interval_minute_to_second = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_bignum_s = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR));
                ptr_bignum_s = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_bignum_u = (SQLTCHAR *) malloc( 1 * STRINGMAX * sizeof(TCHAR));
                ptr_bignum_u = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );

				memset(dt_char_utf8 ,   0, STRINGMAX * sizeof(TCHAR));
                memset(ptr_char_utf8 ,   0, sizeof( SQLLEN ) );
                memset(dt_char_ucs ,   0, STRINGMAX * sizeof(TCHAR));
                memset(ptr_char_ucs ,   0, sizeof( SQLLEN ) );
                memset(dt_varchar_utf8 ,  0,  STRINGMAX * sizeof(TCHAR));
                memset(ptr_varchar_utf8 , 0,   sizeof( SQLLEN ) );
                memset(dt_varchar_ucs ,  0,  STRINGMAX * sizeof(TCHAR));
                memset(ptr_varchar_ucs , 0,   sizeof( SQLLEN ) );
                memset(dt_longvarchar_utf8 , 0,   STRINGMAX * sizeof(TCHAR));
                memset(ptr_longvarchar_utf8 ,0,    sizeof( SQLLEN ) );
                memset(dt_longvarchar_ucs , 0,   STRINGMAX * sizeof(TCHAR));
                memset(ptr_longvarchar_ucs ,0,    sizeof( SQLLEN ) );
                memset(dt_nchar , 0,   STRINGMAX * sizeof(TCHAR) );
                memset(ptr_nchar , 0,   sizeof( SQLLEN ) );
                memset(dt_ncharvarying , 0,   STRINGMAX * sizeof(TCHAR) );
                memset(ptr_ncharvarying , 0,   sizeof( SQLLEN ) );
                memset(dt_decimal_s , 0,   STRINGMAX * sizeof(TCHAR));
                memset(ptr_decimal_s ,0,    sizeof( SQLLEN ) );
                memset(dt_decimal_u , 0,   STRINGMAX * sizeof(TCHAR));
                memset(ptr_decimal_u ,0,    sizeof( SQLLEN ) );
                memset(dt_numeric_s , 0,   STRINGMAX * sizeof(TCHAR));
                memset(ptr_numeric_s , 0,   sizeof( SQLLEN ) );
                memset(dt_numeric_u , 0,   STRINGMAX * sizeof(TCHAR));
                memset(ptr_numeric_u ,0,    sizeof( SQLLEN ) );
                memset(dt_tinyint_s , 0,   STRINGMAX * sizeof(TCHAR) );
                memset(ptr_tinyint_s ,0,    sizeof( SQLLEN ) );
                memset(dt_tinyint_u , 0,   STRINGMAX * sizeof(TCHAR) );
                memset(ptr_tinyint_u ,0,    sizeof( SQLLEN ) );
                memset(dt_smallinteger_s ,0,    STRINGMAX * sizeof(TCHAR) );
                memset(ptr_smallinteger_s ,0,    sizeof( SQLLEN ) );
                memset(dt_smallinteger_u ,0,    STRINGMAX * sizeof(TCHAR) );
                memset(ptr_smallinteger_u ,0,    sizeof( SQLLEN ) );
                memset(dt_integer_s ,0,    STRINGMAX * sizeof(TCHAR) );
                memset(ptr_integer_s ,0,    sizeof( SQLLEN ) );
                memset(dt_integer_u , 0,   STRINGMAX * sizeof(TCHAR) );
                memset(ptr_integer_u , 0,   sizeof( SQLLEN ) );
                memset(dt_largeint , 0,   STRINGMAX * sizeof(TCHAR) );
                memset(ptr_largeint , 0,   sizeof( SQLLEN ) );
                memset(dt_real ,0,    STRINGMAX * sizeof(TCHAR) );
                memset(ptr_real , 0,   sizeof( SQLLEN ) );
                memset(dt_float , 0,   STRINGMAX * sizeof(TCHAR) );
                memset(ptr_float ,0,    sizeof( SQLLEN ) );
                memset(dt_double_precision ,0,    STRINGMAX * sizeof(TCHAR) );
                memset(ptr_double_precision ,0,    sizeof( SQLLEN ) );
                memset(dt_date , 0,   sizeof( DATE_STRUCT ) );
                memset(ptr_date ,0,    sizeof( SQLLEN ) );
                memset(dt_time , 0,   sizeof( TIME_STRUCT ) );
                memset(ptr_time ,  0,  sizeof( SQLLEN ) );
                memset(dt_timestamp , 0,   sizeof( TIMESTAMP_STRUCT ) );
                memset(ptr_timestamp , 0,   sizeof( SQLLEN ) );
                memset(dt_interval_year ,0,    sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_year ,0,    sizeof( SQLLEN ) );
                memset(dt_interval_month ,0,    sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_month , 0,   sizeof( SQLLEN ) );
                memset(dt_interval_day , 0,   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_day ,0,    sizeof( SQLLEN ) );
                memset(dt_interval_hour , 0,   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_hour , 0,   sizeof( SQLLEN ) );
                memset(dt_interval_minute , 0,   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_minute , 0,   sizeof( SQLLEN ) );
                memset(dt_interval_second , 0,   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_second , 0,   sizeof( SQLLEN ) );
                memset(dt_interval_year_to_month , 0,   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_year_to_month , 0,   sizeof( SQLLEN ) );
                memset(dt_interval_day_to_hour , 0,   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_day_to_hour , 0,   sizeof( SQLLEN ) );
                memset(dt_interval_day_to_minute , 0,   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_day_to_minute , 0,   sizeof( SQLLEN ) );
                memset(dt_interval_day_to_second , 0,   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_day_to_second , 0,   sizeof( SQLLEN ) );
                memset(dt_interval_hour_to_minute , 0,   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_hour_to_minute , 0,   sizeof( SQLLEN ) );
                memset(dt_interval_hour_to_second , 0,   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_hour_to_second , 0,   sizeof( SQLLEN ) );
                memset(dt_interval_minute_to_second , 0,   sizeof( SQL_INTERVAL_STRUCT ) );
                memset(ptr_interval_minute_to_second , 0,   sizeof( SQLLEN ) );
                memset(dt_bignum_s , 0,   STRINGMAX * sizeof(TCHAR));
                memset(ptr_bignum_s , 0,   sizeof( SQLLEN ) );
                memset(dt_bignum_u , 0,   STRINGMAX * sizeof(TCHAR));
                memset(ptr_bignum_u ,0,    sizeof( SQLLEN ) );
           }
            break;
    }

    rowsetStatusArray = (SQLUSMALLINT *)malloc ( rowsetSizes * sizeof( SQLUSMALLINT ) );
    rowsetOperationArray  = (SQLUSMALLINT *)malloc ( rowsetSizes * sizeof( SQLUSMALLINT ) );    
    expectedRowsetStatusArray = (SQLUSMALLINT *)malloc ( rowsetSizes * sizeof( SQLUSMALLINT ) );
    memset(rowsetStatusArray , 0, rowsetSizes * sizeof( SQLUSMALLINT ) );
    memset(rowsetOperationArray , 0, rowsetSizes * sizeof( SQLUSMALLINT ) );
    memset(expectedRowsetStatusArray , 0, rowsetSizes * sizeof( SQLUSMALLINT ) );

	// We want all the rows processed.
    for( int loop = 0; loop < rowsetSizes; loop++ )
    {
        rowsetOperationArray[ loop ] = SQL_PARAM_PROCEED;
		expectedRowsetStatusArray[ loop ] = SQL_PARAM_SUCCESS;
    }

    // We need to preset the pointers. 
    for( int loop = 0; loop < rowsetSizes; loop++ )
    {
        switch( bindOrientations )
        {
            case ROW:
            case SINGLE:
                rowset[ loop ].ptr_char_utf8 = SQL_NTS;
                rowset[ loop ].ptr_char_ucs = SQL_NTS;
                rowset[ loop ].ptr_varchar_utf8 = SQL_NTS;
                rowset[ loop ].ptr_varchar_ucs = SQL_NTS;
                rowset[ loop ].ptr_longvarchar_utf8 = SQL_NTS;
                rowset[ loop ].ptr_longvarchar_ucs = SQL_NTS;
                rowset[ loop ].ptr_nchar = SQL_NTS;
                rowset[ loop ].ptr_ncharvarying = SQL_NTS;
                rowset[ loop ].ptr_decimal_s = SQL_NTS;
                rowset[ loop ].ptr_decimal_u = SQL_NTS;
                rowset[ loop ].ptr_numeric_s = SQL_NTS;
                rowset[ loop ].ptr_numeric_u = SQL_NTS;
                rowset[ loop ].ptr_tinyint_s = SQL_NTS;
                rowset[ loop ].ptr_tinyint_u = SQL_NTS;
                rowset[ loop ].ptr_smallinteger_s = SQL_NTS;
                rowset[ loop ].ptr_smallinteger_u = SQL_NTS;
                rowset[ loop ].ptr_integer_s = SQL_NTS;
                rowset[ loop ].ptr_integer_u = SQL_NTS;
                rowset[ loop ].ptr_largeint = SQL_NTS;
                rowset[ loop ].ptr_real = SQL_NTS;
                rowset[ loop ].ptr_float = SQL_NTS;
                rowset[ loop ].ptr_double_precision = SQL_NTS;
                rowset[ loop ].ptr_date = 0;
                rowset[ loop ].ptr_time = 0;
                rowset[ loop ].ptr_timestamp = 0;
                rowset[ loop ].ptr_interval_year = 0;
                rowset[ loop ].ptr_interval_month = 0;
                rowset[ loop ].ptr_interval_day = 0;
                rowset[ loop ].ptr_interval_hour = 0;
                rowset[ loop ].ptr_interval_minute = 0;
                rowset[ loop ].ptr_interval_second = 0;
                rowset[ loop ].ptr_interval_year_to_month = 0;
                rowset[ loop ].ptr_interval_day_to_hour = 0;
                rowset[ loop ].ptr_interval_day_to_minute = 0;
                rowset[ loop ].ptr_interval_day_to_second = 0;
                rowset[ loop ].ptr_interval_hour_to_minute = 0;
                rowset[ loop ].ptr_interval_hour_to_second = 0;
                rowset[ loop ].ptr_interval_minute_to_second = 0;
                rowset[ loop ].ptr_bignum_s = SQL_NTS;
                rowset[ loop ].ptr_bignum_u = SQL_NTS;
                break;
            case COLUMN:
                ptr_char_utf8[ loop ] = SQL_NTS;
                ptr_char_ucs[ loop ] = SQL_NTS;
                ptr_varchar_utf8[ loop ] = SQL_NTS;
                ptr_varchar_ucs[ loop ] = SQL_NTS;
                ptr_longvarchar_utf8[ loop ] = SQL_NTS;
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
                ptr_bignum_s[ loop ] = SQL_NTS;
                ptr_bignum_u[ loop ] = SQL_NTS;
                break;
        }
    }
    return;
 }

 /* Function          : Free rowsets.
   Calling Arguments : int : The test dictates the type of binding orientation that was used.
   Return Arguments  : none

   Description: 
   Frees the data structures we allocate.
 */
 
void FreeRowsets( int bindOrientations )
{
    switch( bindOrientations )
    {
        case ROW:
        case SINGLE:
			if(rowset!=NULL)
			{
				free( rowset ); // <---Got to love row-wise rowsets!
				rowset = NULL;
			}
            break;
        case COLUMN:
            free( dt_char_utf8 );                  free( ptr_char_utf8 );
            free( dt_char_ucs );                  free( ptr_char_ucs );
            free( dt_varchar_utf8 );               free( ptr_varchar_utf8 );
            free( dt_varchar_ucs );               free( ptr_varchar_ucs );
            free( dt_longvarchar_utf8 );           free( ptr_longvarchar_utf8 );
            free( dt_longvarchar_ucs );           free( ptr_longvarchar_ucs );            
            free( dt_nchar );                     free( ptr_nchar );
            free( dt_ncharvarying );              free( ptr_ncharvarying );
            free( dt_decimal_s );                 free( ptr_decimal_s );
            free( dt_decimal_u );                 free( ptr_decimal_u );
            free( dt_numeric_s );                 free( ptr_numeric_s );
            free( dt_numeric_u );                 free( ptr_numeric_u );
            free( dt_tinyint_s );                 free( ptr_tinyint_s );
            free( dt_tinyint_u );                 free( ptr_tinyint_u );
            free( dt_smallinteger_s );            free( ptr_smallinteger_s );
            free( dt_smallinteger_u );            free( ptr_smallinteger_u );
            free( dt_integer_s );                 free( ptr_integer_s );
            free( dt_integer_u );                 free( ptr_integer_u );            
            free( dt_largeint );                  free( ptr_largeint );
            free( dt_real );                      free( ptr_real );
            free( dt_float );                     free( ptr_float );
            free( dt_double_precision );          free( ptr_double_precision );
            free( dt_date );                      free( ptr_date );
            free( dt_time );                      free( ptr_time );
            free( dt_timestamp );                 free( ptr_timestamp );
            free( dt_interval_year );             free( ptr_interval_year );
            free( dt_interval_month );            free( ptr_interval_month );
            free( dt_interval_day );              free( ptr_interval_day );
            free( dt_interval_hour );             free( ptr_interval_hour );
            free( dt_interval_minute );           free( ptr_interval_minute );
            free( dt_interval_second );           free( ptr_interval_second );
            free( dt_interval_year_to_month );    free( ptr_interval_year_to_month );
            free( dt_interval_day_to_hour );      free( ptr_interval_day_to_hour );
            free( dt_interval_day_to_minute );    free( ptr_interval_day_to_minute );
            free( dt_interval_day_to_second );    free( ptr_interval_day_to_second );
            free( dt_interval_hour_to_minute );   free( ptr_interval_hour_to_minute );
            free( dt_interval_hour_to_second );   free( ptr_interval_hour_to_second );
            free( dt_interval_minute_to_second ); free( ptr_interval_minute_to_second );
            free( dt_bignum_s );                  free( ptr_bignum_s );
            free( dt_bignum_u );                  free( ptr_bignum_u );
			break;
    }
    free( rowsetStatusArray );
    free( expectedRowsetStatusArray );
    free( rowsetOperationArray );
    return;
}

bool BindParametersA( int bindOrientations, int actions, int injectionTypes ) {
    SQLRETURN  retcode;
	int offset = 0;

    // Bind the correct parameters based on binding orientation. 
    switch( bindOrientations )
    {
        case ROW:
        case SINGLE:
            // For INSERT SELECT we only bind one column
            if( actions == INSERT_SELECT )
            {
                retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], 2, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                            SQL_BIGINT, 0, 0,
                                            (SQLPOINTER) rowset[ 0 ].dt_largeint, STRINGMAX ,
                                            &rowset[ 0 ].ptr_largeint );
                if( retcode != SQL_SUCCESS )
                {
                    CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                    FreeRowsets( bindOrientations );
                    return false;
                }
                break;
            }

            // For DELETE_PARAM we only bind some specific columns
			if( actions == DELETE_PARAM )
            {
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], 1, SQL_PARAM_INPUT, SQL_C_TCHAR,
											SQL_TCHAR, STRINGMAX - 1, 0,
											(SQLPOINTER) rowset[ 0 ].dt_char_utf8, STRINGMAX - 1 ,
											&rowset[ 0 ].ptr_char_utf8 );
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}
	                   
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], 2, SQL_PARAM_INPUT, SQL_C_TCHAR,
											SQL_TVARCHAR, STRINGMAX, 0,
											(SQLPOINTER) rowset[ 0 ].dt_varchar_utf8, STRINGMAX ,
											&rowset[ 0 ].ptr_varchar_utf8 );                                        
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}
	                
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], 3, SQL_PARAM_INPUT, SQL_C_TCHAR,
											SQL_TLONGVARCHAR, STRINGMAX, 0,
											(SQLPOINTER) rowset[ 0 ].dt_longvarchar_utf8, STRINGMAX ,
											&rowset[ 0 ].ptr_longvarchar_utf8 );                                        
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}
	                
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], 4, SQL_PARAM_INPUT, SQL_C_TCHAR,
											SQL_TLONGVARCHAR, STRINGMAX, 0,
											(SQLPOINTER) rowset[ 0 ].dt_longvarchar_ucs, STRINGMAX ,
											&rowset[ 0 ].ptr_longvarchar_ucs );
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}
	                
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], 5, SQL_PARAM_INPUT, SQL_C_TCHAR,
											SQL_WCHAR, STRINGMAX, 0,
											(SQLPOINTER) rowset[ 0 ].dt_nchar, STRINGMAX,
											&rowset[ 0 ].ptr_nchar );                                        
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}
	                
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], 6, SQL_PARAM_INPUT, SQL_C_TCHAR,
											SQL_WVARCHAR, STRINGMAX, 0,
											(SQLPOINTER) rowset[ 0 ].dt_ncharvarying, STRINGMAX,
											&rowset[ 0 ].ptr_ncharvarying );
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}
                break;
            }

			// Here is where we now bind the C variables to the table columns.
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 1, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_TCHAR, STRINGMAX - 1, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_char_utf8, STRINGMAX - 1 ,
                                        &rowset[ 0 ].ptr_char_utf8 );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 2, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_TCHAR, STRINGMAX, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_char_ucs, STRINGMAX ,
                                        &rowset[ 0 ].ptr_char_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 3, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_TVARCHAR, STRINGMAX, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_varchar_utf8, STRINGMAX ,
                                        &rowset[ 0 ].ptr_varchar_utf8 );                                        
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 4, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_TVARCHAR, STRINGMAX, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_varchar_ucs, STRINGMAX ,
                                        &rowset[ 0 ].ptr_varchar_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 5, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_TLONGVARCHAR, STRINGMAX, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_longvarchar_utf8, STRINGMAX ,
                                        &rowset[ 0 ].ptr_longvarchar_utf8 );                                        
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 6, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_TLONGVARCHAR, STRINGMAX, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_longvarchar_ucs, STRINGMAX ,
                                        &rowset[ 0 ].ptr_longvarchar_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 7, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_WCHAR, STRINGMAX, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_nchar, STRINGMAX,
                                        &rowset[ 0 ].ptr_nchar );                                        
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 8, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_WVARCHAR, STRINGMAX, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_ncharvarying, STRINGMAX,
                                        &rowset[ 0 ].ptr_ncharvarying );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 9, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_DECIMAL, 8, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_decimal_s, STRINGMAX ,
                                        &rowset[ 0 ].ptr_decimal_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 10, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_DECIMAL, 8, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_decimal_u, STRINGMAX ,
                                        &rowset[ 0 ].ptr_decimal_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 11, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_NUMERIC, 8, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_numeric_s, STRINGMAX ,
                                        &rowset[ 0 ].ptr_numeric_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 12, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_NUMERIC, 8, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_numeric_u, STRINGMAX ,
                                        &rowset[ 0 ].ptr_numeric_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 13, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_TINYINT, 0, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_tinyint_s, STRINGMAX ,
                                        &rowset[ 0 ].ptr_tinyint_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 14, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_TINYINT, 0, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_tinyint_u, STRINGMAX ,
                                        &rowset[ 0 ].ptr_tinyint_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                        
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 15, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_SMALLINT, 0, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_smallinteger_s, STRINGMAX ,
                                        &rowset[ 0 ].ptr_smallinteger_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 16, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_SMALLINT, 0, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_smallinteger_u, STRINGMAX ,
                                        &rowset[ 0 ].ptr_smallinteger_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                                             
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 17, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_INTEGER, 0, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_integer_s, STRINGMAX ,
                                        &rowset[ 0 ].ptr_integer_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                        
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 18, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_INTEGER, 0, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_integer_u, STRINGMAX ,
                                        &rowset[ 0 ].ptr_integer_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
            
			if( actions == UPDATE ) {
				offset = -1;
			}
			else {
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 19, SQL_PARAM_INPUT, SQL_C_TCHAR,
											SQL_BIGINT, 0, 0,
											(SQLPOINTER) rowset[ 0 ].dt_largeint, STRINGMAX ,
											&rowset[ 0 ].ptr_largeint );
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}
			}
                     
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 20, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_REAL, 0, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_real, STRINGMAX ,
                                        &rowset[ 0 ].ptr_real );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 21, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_FLOAT, 0, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_float, STRINGMAX ,
                                        &rowset[ 0 ].ptr_float );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                        
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 22, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_DOUBLE, 0, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_double_precision, STRINGMAX ,
                                        &rowset[ 0 ].ptr_double_precision );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }

            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 23, SQL_PARAM_INPUT, SQL_C_TYPE_DATE ,
                                        SQL_TYPE_DATE, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_date, 0,
                                        &rowset[ 0 ].ptr_date );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 24, SQL_PARAM_INPUT, SQL_C_TYPE_TIME ,
                                        SQL_TYPE_TIME, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_time, 0,
                                        &rowset[ 0 ].ptr_time );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 25, SQL_PARAM_INPUT, SQL_C_TYPE_TIMESTAMP ,
                                        SQL_TYPE_TIMESTAMP, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_timestamp, 0,
                                        &rowset[ 0 ].ptr_timestamp );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 26, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_YEAR, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_year,0,
                                        &rowset[ 0 ].ptr_interval_year );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 27, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_MONTH, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_month, 0,
                                        &rowset[ 0 ].ptr_interval_month );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 28, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_DAY, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_day, 0,
                                        &rowset[ 0 ].ptr_interval_day );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 29, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_HOUR, 5, 0,     
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_hour, 0,
                                        &rowset[ 0 ].ptr_interval_hour );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 30, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_MINUTE, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_minute, 0,
                                        &rowset[ 0 ].ptr_interval_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 31, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_SECOND, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_second, 0,
                                        &rowset[ 0 ].ptr_interval_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 32, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_YEAR_TO_MONTH, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_year_to_month, 0,
                                        &rowset[ 0 ].ptr_interval_year_to_month );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 33, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_DAY_TO_HOUR, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_day_to_hour, 0,
                                        &rowset[ 0 ].ptr_interval_day_to_hour );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 34, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_DAY_TO_MINUTE, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_day_to_minute, 0,
                                        &rowset[ 0 ].ptr_interval_day_to_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 35, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_DAY_TO_SECOND, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_day_to_second, 0,
                                        &rowset[ 0 ].ptr_interval_day_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 36, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_HOUR_TO_MINUTE, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_hour_to_minute, 0,
                                        &rowset[ 0 ].ptr_interval_hour_to_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 37, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_HOUR_TO_SECOND, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_hour_to_second, 0,
                                        &rowset[ 0 ].ptr_interval_hour_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 38, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_MINUTE_TO_SECOND, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_minute_to_second, 0,
                                        &rowset[ 0 ].ptr_interval_minute_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
           
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 39, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_NUMERIC, 19, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_bignum_s, STRINGMAX ,
                                        &rowset[ 0 ].ptr_bignum_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 40, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_NUMERIC, 19, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_bignum_u, STRINGMAX ,
                                        &rowset[ 0 ].ptr_bignum_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }

			if( actions == UPDATE ) {
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], 40, SQL_PARAM_INPUT, SQL_C_TCHAR,
											SQL_BIGINT, 0, 0,
											(SQLPOINTER) rowset[ 0 ].dt_largeint, STRINGMAX ,
											&rowset[ 0 ].ptr_largeint );
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}
			}

			break;

        case COLUMN:
			// For DELETE_PARAM we only bind some specific columns
			if( actions == DELETE_PARAM )
            {
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], 1, SQL_PARAM_INPUT, SQL_C_TCHAR,
											SQL_CHAR, STRINGMAX, 0,
											(SQLPOINTER) dt_char_utf8, STRINGMAX*sizeof(TCHAR),
											ptr_char_utf8 );
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}
	                
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], 2, SQL_PARAM_INPUT, SQL_C_TCHAR,
											SQL_VARCHAR, STRINGMAX, 0,
											(SQLPOINTER) dt_varchar_utf8, STRINGMAX*sizeof(TCHAR),
											ptr_varchar_utf8 );                                        
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}
	                
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], 3, SQL_PARAM_INPUT, SQL_C_TCHAR,
											SQL_LONGVARCHAR, STRINGMAX, 0,
											(SQLPOINTER) dt_longvarchar_utf8, STRINGMAX*sizeof(TCHAR),
											ptr_longvarchar_utf8 );                                        
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}
	                
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], 4, SQL_PARAM_INPUT, SQL_C_TCHAR,
											SQL_TLONGVARCHAR, STRINGMAX, 0,
											(SQLPOINTER) dt_longvarchar_ucs, STRINGMAX*sizeof(TCHAR),
											ptr_longvarchar_ucs );
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}
	                
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], 5, SQL_PARAM_INPUT, SQL_C_TCHAR,
											SQL_WCHAR, STRINGMAX, 0,
											(SQLPOINTER) dt_nchar, STRINGMAX*sizeof(TCHAR),
											ptr_nchar );                                        
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}
	                
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], 6, SQL_PARAM_INPUT, SQL_C_TCHAR,
											SQL_WVARCHAR, STRINGMAX, 0,
											(SQLPOINTER) dt_ncharvarying, STRINGMAX*sizeof(TCHAR),
											ptr_ncharvarying );
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}

				break;
			}

            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 1, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_CHAR, STRINGMAX, 0,
                                        (SQLPOINTER) dt_char_utf8, STRINGMAX*sizeof(TCHAR),
                                        ptr_char_utf8 );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 2, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_TCHAR, STRINGMAX, 0,
                                        (SQLPOINTER) dt_char_ucs, STRINGMAX*sizeof(TCHAR),
                                        ptr_char_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 3, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_VARCHAR, STRINGMAX, 0,
                                        (SQLPOINTER) dt_varchar_utf8, STRINGMAX*sizeof(TCHAR),
                                        ptr_varchar_utf8 );                                        
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 4, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_TVARCHAR, STRINGMAX, 0,
                                        (SQLPOINTER) dt_varchar_ucs, STRINGMAX*sizeof(TCHAR),
                                        ptr_varchar_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 5, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_LONGVARCHAR, STRINGMAX, 0,
                                        (SQLPOINTER) dt_longvarchar_utf8, STRINGMAX*sizeof(TCHAR),
                                        ptr_longvarchar_utf8 );                                        
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 6, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_TLONGVARCHAR, STRINGMAX, 0,
                                        (SQLPOINTER) dt_longvarchar_ucs, STRINGMAX*sizeof(TCHAR),
                                        ptr_longvarchar_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 7, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_WCHAR, STRINGMAX, 0,
                                        (SQLPOINTER) dt_nchar, STRINGMAX*sizeof(TCHAR),
                                        ptr_nchar );                                        
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 8, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_WVARCHAR, STRINGMAX, 0,
                                        (SQLPOINTER) dt_ncharvarying, STRINGMAX*sizeof(TCHAR),
                                        ptr_ncharvarying );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 9, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_DECIMAL, 8, 0,
                                        (SQLPOINTER) dt_decimal_s, STRINGMAX*sizeof(TCHAR),
                                        ptr_decimal_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 10, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_DECIMAL, 8, 0,
                                        (SQLPOINTER) dt_decimal_u, STRINGMAX*sizeof(TCHAR),
                                        ptr_decimal_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 11, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_NUMERIC, 8, 0,
                                        (SQLPOINTER) dt_numeric_s, STRINGMAX*sizeof(TCHAR),
                                        ptr_numeric_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 12, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_NUMERIC, 8, 0,
                                        (SQLPOINTER) dt_numeric_u, STRINGMAX*sizeof(TCHAR),
                                        ptr_numeric_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 13, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_TINYINT, 0, 0,
                                        (SQLPOINTER) dt_tinyint_s, STRINGMAX*sizeof(TCHAR),
                                        ptr_tinyint_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 14, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_TINYINT, 0, 0,
                                        (SQLPOINTER) dt_tinyint_u, STRINGMAX*sizeof(TCHAR),
                                        ptr_tinyint_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                        
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 15, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_SMALLINT, 0, 0,
                                        (SQLPOINTER) dt_smallinteger_s, STRINGMAX*sizeof(TCHAR),
                                        ptr_smallinteger_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 16, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_SMALLINT, 0, 0,
                                        (SQLPOINTER) dt_smallinteger_u, STRINGMAX*sizeof(TCHAR),
                                        ptr_smallinteger_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                                             
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 17, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_INTEGER, 0, 0,
                                        (SQLPOINTER) dt_integer_s, STRINGMAX*sizeof(TCHAR),
                                        ptr_integer_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                        
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 18, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_INTEGER, 0, 0,
                                        (SQLPOINTER) dt_integer_u, STRINGMAX*sizeof(TCHAR),
                                        ptr_integer_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
            
			if (actions == UPDATE) {
				offset = -1;
			}
			else {
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 19, SQL_PARAM_INPUT, SQL_C_TCHAR,
											SQL_BIGINT, 0, 0,
											(SQLPOINTER) dt_largeint, STRINGMAX*sizeof(TCHAR),
											ptr_largeint );
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}
			}
                     
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 20, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_REAL, 0, 0,
                                        (SQLPOINTER) dt_real, STRINGMAX*sizeof(TCHAR),
                                        ptr_real );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 21, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_FLOAT, 0, 0,
                                        (SQLPOINTER) dt_float, STRINGMAX*sizeof(TCHAR),
                                        ptr_float );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                        
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 22, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_DOUBLE, 0, 0,
                                        (SQLPOINTER) dt_double_precision, STRINGMAX*sizeof(TCHAR),
                                        ptr_double_precision );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                                                                                     
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 23, SQL_PARAM_INPUT, SQL_C_TYPE_DATE ,
                                        SQL_TYPE_DATE, 5, 0, 
                                        (SQLPOINTER) dt_date, 0,
                                        ptr_date );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 24, SQL_PARAM_INPUT, SQL_C_TYPE_TIME ,
                                        SQL_TYPE_TIME, 5, 0, 
                                        (SQLPOINTER) dt_time, 0,
                                        ptr_time );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 25, SQL_PARAM_INPUT, SQL_C_TYPE_TIMESTAMP ,
                                        SQL_TYPE_TIMESTAMP, 5, 0, 
                                        (SQLPOINTER) dt_timestamp, 0,
                                        ptr_timestamp );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 26, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_YEAR, 5, 0, 
                                        (SQLPOINTER) dt_interval_year,0,
                                        ptr_interval_year );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 27, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_MONTH, 5, 0, 
                                        (SQLPOINTER) dt_interval_month, 0,
                                        ptr_interval_month );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 28, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_DAY, 5, 0, 
                                        (SQLPOINTER) dt_interval_day, 0,
                                        ptr_interval_day );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 29, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_HOUR, 5, 0, 
                                        (SQLPOINTER) dt_interval_hour, 0,
                                        ptr_interval_hour );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 30, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_MINUTE, 5, 0, 
                                        (SQLPOINTER) dt_interval_minute, 0,
                                        ptr_interval_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 31, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_SECOND, 5, 0, 
                                        (SQLPOINTER) dt_interval_second, 0,
                                        ptr_interval_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 32, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_YEAR_TO_MONTH, 5, 0, 
                                        (SQLPOINTER) dt_interval_year_to_month, 0,
                                        ptr_interval_year_to_month );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 33, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_DAY_TO_HOUR, 5, 0, 
                                        (SQLPOINTER) dt_interval_day_to_hour, 0,
                                        ptr_interval_day_to_hour );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 34, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_DAY_TO_MINUTE, 5, 0, 
                                        (SQLPOINTER) dt_interval_day_to_minute, 0,
                                        ptr_interval_day_to_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 35, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_DAY_TO_SECOND, 5, 0, 
                                        (SQLPOINTER) dt_interval_day_to_second, 0,
                                        ptr_interval_day_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 36, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_HOUR_TO_MINUTE, 5, 0, 
                                        (SQLPOINTER) dt_interval_hour_to_minute, 0,
                                        ptr_interval_hour_to_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 37, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_HOUR_TO_SECOND, 5, 0, 
                                        (SQLPOINTER) dt_interval_hour_to_second, 0,
                                        ptr_interval_hour_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 38, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_MINUTE_TO_SECOND, 5, 0, 
                                        (SQLPOINTER) dt_interval_minute_to_second, 0,
                                        ptr_interval_minute_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }

            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 39, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_NUMERIC, 19, 0,
                                        (SQLPOINTER) dt_bignum_s, STRINGMAX*sizeof(TCHAR) ,
                                        ptr_bignum_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 40, SQL_PARAM_INPUT, SQL_C_TCHAR,
                                        SQL_NUMERIC, 19, 0,
                                        (SQLPOINTER) dt_bignum_u, STRINGMAX*sizeof(TCHAR),
                                        ptr_bignum_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }

			if (actions == UPDATE) {
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], 40, SQL_PARAM_INPUT, SQL_C_TCHAR,
											SQL_BIGINT, 0, 0,
											(SQLPOINTER) dt_largeint, STRINGMAX*sizeof(TCHAR),
											ptr_largeint );
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( _T("SQLBindParameter()"), __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}
			}

			break;
    }

	return true;
}

bool BindColsA( int bindOrientations ) {
	SQLRETURN  retcode;

	switch( bindOrientations )
    {
        case SINGLE:
        case ROW:
            // Here is where we now bind the C variables to the table columns.
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 1,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_char_utf8, STRINGMAX,
                                  &rowset[ 0 ].ptr_char_utf8 );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 2,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_char_ucs, STRINGMAX,
                                  &rowset[ 0 ].ptr_char_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 3,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_varchar_utf8, STRINGMAX,
                                  &rowset[ 0 ].ptr_varchar_utf8 );                                  
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 4,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_varchar_ucs, STRINGMAX,
                                  &rowset[ 0 ].ptr_varchar_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 5,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_longvarchar_utf8, STRINGMAX,
                                  &rowset[ 0 ].ptr_longvarchar_utf8 );                                  
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 6,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_longvarchar_ucs, STRINGMAX,
                                  &rowset[ 0 ].ptr_longvarchar_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 7,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_nchar, STRINGMAX,
                                  &rowset[ 0 ].ptr_nchar );                                  
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 8,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_ncharvarying, STRINGMAX,
                                  &rowset[ 0 ].ptr_ncharvarying );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 9,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_decimal_s, STRINGMAX,
                                  &rowset[ 0 ].ptr_decimal_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 10,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_decimal_u, STRINGMAX,
                                  &rowset[ 0 ].ptr_decimal_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 11,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_numeric_s, STRINGMAX,
                                  &rowset[ 0 ].ptr_numeric_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 12,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_numeric_u, STRINGMAX,
                                  &rowset[ 0 ].ptr_numeric_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                               
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 13,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_tinyint_s, STRINGMAX,
                                  &rowset[ 0 ].ptr_tinyint_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 14,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_tinyint_u, STRINGMAX,
                                  &rowset[ 0 ].ptr_tinyint_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                  
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 15,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_smallinteger_s, STRINGMAX,
                                  &rowset[ 0 ].ptr_smallinteger_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 16,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_smallinteger_u, STRINGMAX,
                                  &rowset[ 0 ].ptr_smallinteger_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                                       
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 17,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_integer_s, STRINGMAX,
                                  &rowset[ 0 ].ptr_integer_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                  
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 18,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_integer_u, STRINGMAX,
                                  &rowset[ 0 ].ptr_integer_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                  
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 19,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_largeint, STRINGMAX,
                                  &rowset[ 0 ].ptr_largeint );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                     
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 20,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_real, STRINGMAX,
                                  &rowset[ 0 ].ptr_real );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 21,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_float, STRINGMAX,
                                  &rowset[ 0 ].ptr_float );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                  
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 22,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_double_precision, STRINGMAX,
                                  &rowset[ 0 ].ptr_double_precision );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                  
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 23,  SQL_C_TYPE_DATE ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_date, 0,
                                  &rowset[ 0 ].ptr_date );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 24,  SQL_C_TYPE_TIME ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_time, 0,
                                  &rowset[ 0 ].ptr_time );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 25,  SQL_C_TYPE_TIMESTAMP ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_timestamp, 0,
                                  &rowset[ 0 ].ptr_timestamp );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 26,  SQL_C_INTERVAL_YEAR ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_year,0,
                                  &rowset[ 0 ].ptr_interval_year );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 27,  SQL_C_INTERVAL_MONTH ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_month, 0,
                                  &rowset[ 0 ].ptr_interval_month );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 28,  SQL_C_INTERVAL_DAY ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_day, 0,
                                  &rowset[ 0 ].ptr_interval_day );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 29,  SQL_C_INTERVAL_HOUR ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_hour, 0,
                                  &rowset[ 0 ].ptr_interval_hour );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 30,  SQL_C_INTERVAL_MINUTE ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_minute, 0,
                                  &rowset[ 0 ].ptr_interval_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 31,  SQL_C_INTERVAL_SECOND ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_second, 0,
                                  &rowset[ 0 ].ptr_interval_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 32,  SQL_C_INTERVAL_YEAR_TO_MONTH ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_year_to_month, 0,
                                  &rowset[ 0 ].ptr_interval_year_to_month );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 33,  SQL_C_INTERVAL_DAY_TO_HOUR ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_day_to_hour, 0,
                                  &rowset[ 0 ].ptr_interval_day_to_hour );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 34,  SQL_C_INTERVAL_DAY_TO_MINUTE ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_day_to_minute, 0,
                                  &rowset[ 0 ].ptr_interval_day_to_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 35,  SQL_C_INTERVAL_DAY_TO_SECOND ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_day_to_second, 0,
                                  &rowset[ 0 ].ptr_interval_day_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 36,  SQL_C_INTERVAL_HOUR_TO_MINUTE ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_hour_to_minute, 0,
                                  &rowset[ 0 ].ptr_interval_hour_to_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 37,  SQL_C_INTERVAL_HOUR_TO_SECOND ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_hour_to_second, 0,
                                  &rowset[ 0 ].ptr_interval_hour_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 38,  SQL_C_INTERVAL_MINUTE_TO_SECOND ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_minute_to_second, 0,
                                  &rowset[ 0 ].ptr_interval_minute_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }

            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 39,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_bignum_s, STRINGMAX,
                                  &rowset[ 0 ].ptr_bignum_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 40,  SQL_C_TCHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_bignum_u, STRINGMAX,
                                  &rowset[ 0 ].ptr_bignum_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }

			break;
        case COLUMN:
            // Here is where we now bind the C variables to the table columns.
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 1,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_char_utf8, STRINGMAX*sizeof(TCHAR),
                                  ptr_char_utf8 );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 2,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_char_ucs, STRINGMAX*sizeof(TCHAR),
                                  ptr_char_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 3,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_varchar_utf8, STRINGMAX*sizeof(TCHAR),
                                  ptr_varchar_utf8 );                                  
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 4,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_varchar_ucs, STRINGMAX*sizeof(TCHAR),
                                  ptr_varchar_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 5,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_longvarchar_utf8, STRINGMAX*sizeof(TCHAR),
                                  ptr_longvarchar_utf8 );                                  
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 6,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_longvarchar_ucs, STRINGMAX*sizeof(TCHAR),
                                  ptr_longvarchar_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 7,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_nchar, STRINGMAX*sizeof(TCHAR),
                                  ptr_nchar );                                  
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 8,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_ncharvarying, STRINGMAX*sizeof(TCHAR),
                                  ptr_ncharvarying );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 9,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_decimal_s, STRINGMAX*sizeof(TCHAR),
                                  ptr_decimal_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 10,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_decimal_u, STRINGMAX*sizeof(TCHAR),
                                  ptr_decimal_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 11,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_numeric_s, STRINGMAX*sizeof(TCHAR),
                                  ptr_numeric_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 12,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_numeric_u, STRINGMAX*sizeof(TCHAR),
                                  ptr_numeric_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                               
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 13,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_tinyint_s, STRINGMAX*sizeof(TCHAR),
                                  ptr_tinyint_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 14,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_tinyint_u, STRINGMAX*sizeof(TCHAR),
                                  ptr_tinyint_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                  
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 15,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_smallinteger_s, STRINGMAX*sizeof(TCHAR),
                                  ptr_smallinteger_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 16,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_smallinteger_u, STRINGMAX*sizeof(TCHAR),
                                  ptr_smallinteger_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                                       
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 17,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_integer_s, STRINGMAX*sizeof(TCHAR),
                                  ptr_integer_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                  
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 18,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_integer_u, STRINGMAX*sizeof(TCHAR),
                                  ptr_integer_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                  
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 19,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_largeint, STRINGMAX*sizeof(TCHAR),
                                  ptr_largeint );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                     
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 20,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_real, STRINGMAX*sizeof(TCHAR),
                                  ptr_real );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 21,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_float, STRINGMAX*sizeof(TCHAR),
                                  ptr_float );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                  
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 22,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_double_precision, STRINGMAX*sizeof(TCHAR),
                                  ptr_double_precision );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                                                                         
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 23,  SQL_C_TYPE_DATE ,
                                  (SQLPOINTER) dt_date, 0,
                                  ptr_date );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 24,  SQL_C_TYPE_TIME ,
                                  (SQLPOINTER) dt_time, 0,
                                  ptr_time );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 25,  SQL_C_TYPE_TIMESTAMP ,
                                  (SQLPOINTER) dt_timestamp, 0,
                                  ptr_timestamp );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 26,  SQL_C_INTERVAL_YEAR ,
                                  (SQLPOINTER) dt_interval_year,0,
                                  ptr_interval_year );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 27,  SQL_C_INTERVAL_MONTH ,
                                  (SQLPOINTER) dt_interval_month, 0,
                                  ptr_interval_month );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 28,  SQL_C_INTERVAL_DAY ,
                                  (SQLPOINTER) dt_interval_day, 0,
                                  ptr_interval_day );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 29,  SQL_C_INTERVAL_HOUR ,
                                  (SQLPOINTER) dt_interval_hour, 0,
                                  ptr_interval_hour );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 30,  SQL_C_INTERVAL_MINUTE ,
                                  (SQLPOINTER) dt_interval_minute, 0,
                                  ptr_interval_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 31,  SQL_C_INTERVAL_SECOND ,
                                  (SQLPOINTER) dt_interval_second, 0,
                                  ptr_interval_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 32,  SQL_C_INTERVAL_YEAR_TO_MONTH ,
                                  (SQLPOINTER) dt_interval_year_to_month, 0,
                                  ptr_interval_year_to_month );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 33,  SQL_C_INTERVAL_DAY_TO_HOUR ,
                                  (SQLPOINTER) dt_interval_day_to_hour, 0,
                                  ptr_interval_day_to_hour );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 34,  SQL_C_INTERVAL_DAY_TO_MINUTE ,
                                  (SQLPOINTER) dt_interval_day_to_minute, 0,
                                  ptr_interval_day_to_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 35,  SQL_C_INTERVAL_DAY_TO_SECOND ,
                                  (SQLPOINTER) dt_interval_day_to_second, 0,
                                  ptr_interval_day_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 36,  SQL_C_INTERVAL_HOUR_TO_MINUTE ,
                                  (SQLPOINTER) dt_interval_hour_to_minute, 0,
                                  ptr_interval_hour_to_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 37,  SQL_C_INTERVAL_HOUR_TO_SECOND ,
                                  (SQLPOINTER) dt_interval_hour_to_second, 0,
                                  ptr_interval_hour_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 38,  SQL_C_INTERVAL_MINUTE_TO_SECOND ,
                                  (SQLPOINTER) dt_interval_minute_to_second, 0,
                                  ptr_interval_minute_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }

	        retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 39,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_bignum_s, STRINGMAX*sizeof(TCHAR),
                                  ptr_bignum_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 40,  SQL_C_TCHAR,
                                  (SQLPOINTER) dt_bignum_u, STRINGMAX*sizeof(TCHAR),
                                  ptr_bignum_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( _T("SQLBindCol()"), __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }

			break;
    }

	return true;
}

void assignStatus (int rowsetPos, SQLUSMALLINT status)
{
	if (expectedRowsetStatusArray[ rowsetPos ] == SQL_PARAM_SUCCESS)
	{
		expectedRowsetStatusArray[ rowsetPos ] = status;
	}
	else if (expectedRowsetStatusArray[ rowsetPos ] == SQL_PARAM_SUCCESS_WITH_INFO)
	{
		if (status == SQL_PARAM_ERROR)
			expectedRowsetStatusArray[ rowsetPos ] = status;
	}
}

void DML_A_ROW (unsigned int bitflag,
				int actions,
				int tableTypes,
				int bindTypes,
				int rs,
				int *failureInjectionCount,
				int numberOfRowsHandled)
{

	switch ( actions ) {
		case INSERT:
			AssignRow( rs, numberOfRowsHandled + 1, numberOfRowsHandled + 1 );
			break;
		case UPDATE:
			AssignRow( rs, 2, numberOfRowsHandled + 1 );
			break;
		case DELETE_PARAM:
			AssignRow( rs, numberOfRowsHandled + 1, numberOfRowsHandled + 1 );
			break;
		default:
			break;
	}

	/**********************************************************************************/
	/**********************************************************************************/
	if ((bitflag & B_NOERRORS) == B_NOERRORS)
	{
		AssignRow( rs, numberOfRowsHandled + 1, numberOfRowsHandled + 1 );
		assignStatus( rs, SQL_PARAM_SUCCESS );
	}
	/**********************************************************************************/
	/**********************************************************************************/
	if ((bitflag & B_DUPLICATEKEY) == B_DUPLICATEKEY)
	{
		AssignRow( rs, 2, numberOfRowsHandled + 1 );
		switch ( actions ) {
			case INSERT:
				if ( tableTypes == MULTISET 
					/* SQ */
                    || (injectionTypes[ unitTest.injectionType ] == ERR_PER_ROW && rs == 2)
                    || (injectionTypes[ unitTest.injectionType ] == FULL_ERRORS && rs == 2)
					/* end of SQ */
					)
					assignStatus( rs, SQL_PARAM_SUCCESS );
				else {
					assignStatus( rs, SQL_PARAM_ERROR );
					(*failureInjectionCount)++;
				}
				break;
			case UPDATE:
				assignStatus( rs, SQL_PARAM_SUCCESS );
				break;
			case DELETE_PARAM:
				assignStatus( rs, SQL_PARAM_SUCCESS );
				(*failureInjectionCount)++;
				break;
			default:
				break;
		}
	}
	/**********************************************************************************/
	/**********************************************************************************/
	if ((bitflag & B_DUPLICATEROW) == B_DUPLICATEROW)
	{
		AssignRow( rs, 2, 2 );
		switch ( actions ) {
			case INSERT:
				if (( tableTypes == MULTISET ) ||
					( tableTypes == SET && errorChecking != MODE_SPECIAL_1 ))
					assignStatus( rs, SQL_PARAM_SUCCESS );
				else
					assignStatus( rs, SQL_PARAM_ERROR );
				(*failureInjectionCount)++;
				break;
			case UPDATE:
				assignStatus( rs, SQL_PARAM_SUCCESS );
				break;
			case DELETE_PARAM:
				assignStatus( rs, SQL_PARAM_SUCCESS );
				(*failureInjectionCount)++;
				break;
			default:
				break;
		}
	}
	/**********************************************************************************/
	/**********************************************************************************/
	if ((bitflag & B_STRINGOVERFLOW) == B_STRINGOVERFLOW)
	{
		switch( bindTypes )
		{
			case ROW:
			case SINGLE:
				swprintf( (TCHAR*)rowset[ rs ].dt_char_ucs,256, _T("%s"), String_OverFlow );
				swprintf( (TCHAR*)rowset[ rs ].dt_varchar_ucs,256, _T("%s"), String_OverFlow );
				break;
			case COLUMN:
				_stprintf( (TCHAR*)&dt_char_ucs[ rs * STRINGMAX  ], _T("%s"), String_OverFlow );
				_stprintf( (TCHAR*)&dt_varchar_ucs[ rs * STRINGMAX  ], _T("%s"), String_OverFlow );
				break;
		}
		switch ( actions ) {
			case INSERT:
			case UPDATE:
				/* SQ assignStatus( rs, SQL_PARAM_SUCCESS_WITH_INFO ); */ assignStatus( rs, SQL_PARAM_ERROR);
				/* SQ new */ (*failureInjectionCount)++;
				break;
			case DELETE_PARAM:
				assignStatus( rs, SQL_PARAM_SUCCESS );
				(*failureInjectionCount)++;
				break;
			default:
				break;
		}
	}
	/**********************************************************************************/
	/**********************************************************************************/
	if ((bitflag & B_CHECKCONST) == B_CHECKCONST)
	{
		switch( bindTypes )
		{
			case ROW:
			case SINGLE:
           		swprintf( (TCHAR*)rowset[ rs ].dt_integer_s, 256, _T("%d"), 50001 );
				break;
			case COLUMN:
           		_stprintf( (TCHAR*)&dt_integer_s[ rs * STRINGMAX  ], _T("%d"), 50001 );
				break;
		}
		switch ( actions ) {
			case INSERT:
			case UPDATE:
				assignStatus( rs, SQL_PARAM_ERROR );
				(*failureInjectionCount)++;
				break;
			case DELETE_PARAM:
				assignStatus( rs, SQL_PARAM_SUCCESS );
				(*failureInjectionCount)++;
				break;
			default:
				break;
		}
	}
	/**********************************************************************************/
	/**********************************************************************************/
	if ((bitflag & B_NULLVALUE) == B_NULLVALUE)
	{
		switch( bindTypes )
		{
			case ROW:
			case SINGLE:
				rowset[ rs ].dt_integer_s[ 0 ] = '\0'; rowset[ rs ].ptr_integer_s = SQL_NULL_DATA;
				break;
			case COLUMN:
				dt_integer_s[ rs * STRINGMAX ] = '\0'; ptr_integer_s[ rs ] = SQL_NULL_DATA;
				break;
		}
		switch ( actions ) {
			case INSERT:
			case UPDATE:
				assignStatus( rs, SQL_PARAM_ERROR );
				(*failureInjectionCount)++;
				break;
			case DELETE_PARAM:
				assignStatus( rs, SQL_PARAM_SUCCESS );
				(*failureInjectionCount)++;
				break;
			default:
				break;
		}
	}
	/**********************************************************************************/
	/**********************************************************************************/
	if ((bitflag & B_NUMERICOVERFLOW) == B_NUMERICOVERFLOW)
	{
		switch( bindTypes )
		{
			case ROW:
			case SINGLE:
	            swprintf( (TCHAR*)rowset[ rs ].dt_decimal_s, 256, _T("%d"), 123456789 );
				break;
			case COLUMN:
	            _stprintf( (TCHAR*)&dt_decimal_s[ rs * STRINGMAX  ], _T("%d"), 123456789 );
				break;
		}
		switch ( actions ) {
			case INSERT:
			case UPDATE:
				assignStatus( rs, SQL_PARAM_ERROR );
				(*failureInjectionCount)++;
				break;
			case DELETE_PARAM:
				assignStatus( rs, SQL_PARAM_SUCCESS );
				(*failureInjectionCount)++;
				break;
			default:
				break;
		}
	}
	/**********************************************************************************/
	/**********************************************************************************/
	if ((bitflag & B_SIGN2UNSIGN) == B_SIGN2UNSIGN)
	{
		switch( bindTypes )
		{
			case ROW:
			case SINGLE:
	            swprintf( (TCHAR*)rowset[ rs ].dt_decimal_u, 256, _T("%d"), -1);
				break;
			case COLUMN:
	            _stprintf( (TCHAR*)&dt_decimal_u[ rs * STRINGMAX  ], _T("%d"), -1 );
				break;
		}
		switch ( actions ) {
			case INSERT:
			case UPDATE:
				assignStatus( rs, SQL_PARAM_ERROR );
				(*failureInjectionCount)++;
				break;
			case DELETE_PARAM:
				assignStatus( rs, SQL_PARAM_SUCCESS );
				(*failureInjectionCount)++;
				break;
			default:
				break;
		}
	}
	/**********************************************************************************/
	/**********************************************************************************/
	if ((bitflag & B_TIMESTAMP) == B_TIMESTAMP)
	{
		switch( bindTypes )
		{
			case ROW:
			case SINGLE:
				rowset[ rs ].dt_timestamp.day = 32;
				break;
			case COLUMN:
				dt_timestamp[ rs ].day = 32;
				break;
		}
		switch ( actions ) {
			case INSERT:
			case UPDATE:
				assignStatus( rs, SQL_PARAM_ERROR );
				(*failureInjectionCount)++;
				break;
			case DELETE_PARAM:
				assignStatus( rs, SQL_PARAM_SUCCESS );
				(*failureInjectionCount)++;
				break;
			default:
				break;
		}
	}
	/**********************************************************************************/
	/**********************************************************************************/
	if ((bitflag & B_DIVIDEDBYZERO) == B_DIVIDEDBYZERO)
	{
	}
}

/*There functions are added for Character Sets testing
Added by HP
*/
int next_line(TCHAR *lineOut, FILE *scriptFD) {
	int p = 0, c = 0;
	TCHAR buff[2048];
	_tcscpy(lineOut,_T(""));
	while (_fgetts(buff , 2048 , scriptFD) != NULL) {
		//trim
		p = (int)_tcslen(buff)-1;
		while (buff[p] == ' ' || buff[p] == '\n' || buff[p] == '\r' || buff[p] == '\t') p--;
		buff[p+1] = '\0';

		p = 0;
		while (buff[p] == ' ' || buff[p] == '\n'  || buff[p] == '\r' || buff[p] == '\t') p++;
		if (buff[p] == '\0') continue;
		if (buff[p] == '-' && buff[p+1] == '-') continue;


		//copy to buffer
		c = 0;
		do {
			lineOut[c++] = buff[p];
		}
		while (buff[p++] != '\0');

		return TRUE;
	}
	return FALSE;
}

var_list_t* load_api_vars(TCHAR *api, TCHAR *textFile) {
	TCHAR		line[5120];
	FILE		*scriptFD;
	var_list_t *my_var_list = NULL;
	int i, p, num_vars = 0;
	int found = FALSE;
	TCHAR strAPI[256];
	TCHAR seps[]   = _T("\"");
	TCHAR *token;

	if ((scriptFD = _tfopen(textFile, _T("r"))) == NULL) {
		_tprintf(_T("Error open script file %s\n"), textFile);
		return NULL;
	}

	//Find the API block in text file
	swprintf(strAPI, 256, _T("[%s "), api);
	while (next_line(line, scriptFD)) {
		if (_tcsnicmp(strAPI, line, _tcslen(strAPI)) == 0) {
			num_vars = _tstoi(line + _tcslen(strAPI));
			found = TRUE;
			break;
		}
	}
	if (!found) {
		fclose(scriptFD);
		_tprintf(_T("Could not find API name %s in the text file %s!\n"), api, textFile);
		return NULL;
	}

	if (!found || num_vars == 0) {
		fclose(scriptFD);
		_tprintf(_T("Can not find API %s. Or number of variables is %d\n"), api, num_vars);
		return NULL;
	}

	//Allocate mem for variables
	my_var_list = (var_list_t*)malloc(num_vars*sizeof(var_list_t));
	if (my_var_list == NULL) {
		fclose(scriptFD);
		_tprintf(_T("Malloc memory error!\n"));
		return NULL;
	}

	//Scan each vars and load to memory
	swprintf(strAPI, 256, _T("[END]"));
	i = 0; found = FALSE;
	while (next_line(line, scriptFD)) {
		if (_tcsnicmp(strAPI, line, _tcslen(strAPI)) == 0) {
			found = TRUE;
			break;
		}
		if (i>=num_vars) {
			i++;
			break;
		}

		token = _tcstok(_tcsdup(line), seps);
		my_var_list[i].value = _tcsdup(line + _tcslen(token) + 1);
		p = (int)_tcslen(my_var_list[i].value)-1;
		if (my_var_list[i].value[p] == '"') {
			my_var_list[i].value[p] = '\0';
		}
		else {
			fclose(scriptFD);
			_tprintf(_T("File format error! Variable string must be ended by a double quote. :::%c:::\n"), my_var_list[i].value[p]);
			_tprintf(_T("File name: %s\nAPI block: %s\nVariable ID: %s\n"), textFile, api, token);
			return NULL;
		}
		
		p = (int)_tcslen(token)-1;
		while (token[p] == ' ' || token[p] == '\t') p--;
		token[p+1] = '\0';
		my_var_list[i].var_name = _tcsdup(token);

		if (i == (num_vars-1)) my_var_list[i].last = TRUE;
		else my_var_list[i].last = FALSE;

		i++;
	}

	if(i != num_vars) {
		fclose(scriptFD);
		_tprintf(_T("The number specified for API %s doesn't match with number of variables declared!\n"), api);
		return NULL;
	}
	if (!found) {
		fclose(scriptFD);
		_tprintf(_T("The variable block of API %s is not teminated by a marker [END].")
				_T(" OR the text file %s is in wrong format!\n"), api, textFile);
		return NULL;
	}

	fclose(scriptFD);
	return my_var_list;
}

void print_list (var_list_t *var_list) {
	int i=0;
	if (var_list == NULL) return;
	do {
		_tprintf(_T("Name: :%s:\n"), var_list[i].var_name);
		_tprintf(_T("Value: :%s:\n"), var_list[i].value);
		_tprintf(_T("Last: %i\n"), var_list[i].last);
	} while(!var_list[i++].last);
	_tprintf(_T("=============================================\n"));
}

void free_list (var_list_t *var_list) {
	int i=0;
	if (var_list == NULL) return;
	do {
		free(var_list[i].var_name);
		free(var_list[i].value);
	} while(!var_list[i++].last);

	free(var_list);
}

TCHAR* var_mapping(TCHAR *var_name, var_list_t *var_list) {
	int i=0;
	if (var_list == NULL) return NULL;
	do {
		if(_tcsicmp(var_name, var_list[i].var_name) == 0) {
			return var_list[i].value;
		}
	} while(!var_list[i++].last);
	_tprintf(_T("Mapping error: Can not find variable name %s\n"), var_name);
	return NULL;
}

void DisplayTable(int bindOrientations, int numRows) {
	int i = 0;
	while(i < numRows)
		DisplayRowsets(bindOrientations, i++);
}

#endif /* ROWSETS_H */
