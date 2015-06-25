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

#define ARGS                        "d:u:p:o:t:r:m:s:"

#define STRINGMAX                   256
#define STRINGMAXDBL                41
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
    SQLCHAR             dt_char_iso[STRINGMAX];           SQLLEN ptr_char_iso;
    SQLCHAR             dt_char_ucs[STRINGMAXDBL];        SQLLEN ptr_char_ucs;
    SQLCHAR             dt_varchar_iso[STRINGMAX];        SQLLEN ptr_varchar_iso;
    SQLCHAR             dt_varchar_ucs[STRINGMAXDBL];     SQLLEN ptr_varchar_ucs;
    SQLCHAR             dt_longvarchar_iso[STRINGMAX];    SQLLEN ptr_longvarchar_iso;
    SQLCHAR             dt_longvarchar_ucs[STRINGMAXDBL]; SQLLEN ptr_longvarchar_ucs;            
    SQLCHAR             dt_nchar[STRINGMAXDBL];           SQLLEN ptr_nchar;
    SQLCHAR             dt_ncharvarying[STRINGMAXDBL];    SQLLEN ptr_ncharvarying;
    SQLCHAR             dt_decimal_s[STRINGMAX];          SQLLEN ptr_decimal_s;
    SQLCHAR             dt_decimal_u[STRINGMAX];          SQLLEN ptr_decimal_u;
    SQLCHAR             dt_numeric_s[STRINGMAX];          SQLLEN ptr_numeric_s;
    SQLCHAR             dt_numeric_u[STRINGMAX];          SQLLEN ptr_numeric_u;
    SQLCHAR             dt_tinyint_s[STRINGMAX];          SQLLEN ptr_tinyint_s;
    SQLCHAR             dt_tinyint_u[STRINGMAX];          SQLLEN ptr_tinyint_u;
    SQLCHAR             dt_smallinteger_s[STRINGMAX];     SQLLEN ptr_smallinteger_s;
    SQLCHAR             dt_smallinteger_u[STRINGMAX];     SQLLEN ptr_smallinteger_u;
    SQLCHAR             dt_integer_s[STRINGMAX];          SQLLEN ptr_integer_s;
    SQLCHAR             dt_integer_u[STRINGMAX];          SQLLEN ptr_integer_u;            
    SQLCHAR             dt_largeint[STRINGMAX];           SQLLEN ptr_largeint;
    SQLCHAR             dt_real[STRINGMAX];               SQLLEN ptr_real;
    SQLCHAR             dt_float[STRINGMAX];              SQLLEN ptr_float;
    SQLCHAR             dt_double_precision[STRINGMAX];   SQLLEN ptr_double_precision;
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
    SQLCHAR             dt_bignum_s[STRINGMAX];           SQLLEN ptr_bignum_s;
    SQLCHAR             dt_bignum_u[STRINGMAX];           SQLLEN ptr_bignum_u;
} table_rowset;

// These variables are simular to the fields in the above structure but are used
// for column-wise binding.
SQLCHAR             *dt_char_iso;                   SQLLEN *ptr_char_iso;
SQLCHAR             *dt_char_ucs;                   SQLLEN *ptr_char_ucs;
SQLCHAR             *dt_varchar_iso;                SQLLEN *ptr_varchar_iso;
SQLCHAR             *dt_varchar_ucs;                SQLLEN *ptr_varchar_ucs;
SQLCHAR             *dt_longvarchar_iso;            SQLLEN *ptr_longvarchar_iso;
SQLCHAR             *dt_longvarchar_ucs;            SQLLEN *ptr_longvarchar_ucs;            
SQLCHAR             *dt_nchar;                      SQLLEN *ptr_nchar;
SQLCHAR             *dt_ncharvarying;               SQLLEN *ptr_ncharvarying;
SQLCHAR             *dt_decimal_s;                  SQLLEN *ptr_decimal_s;
SQLCHAR             *dt_decimal_u;                  SQLLEN *ptr_decimal_u;
SQLCHAR             *dt_numeric_s;                  SQLLEN *ptr_numeric_s;
SQLCHAR             *dt_numeric_u;                  SQLLEN *ptr_numeric_u;
SQLCHAR             *dt_tinyint_s;                  SQLLEN *ptr_tinyint_s;
SQLCHAR             *dt_tinyint_u;                  SQLLEN *ptr_tinyint_u;
SQLCHAR             *dt_smallinteger_s;             SQLLEN *ptr_smallinteger_s;
SQLCHAR             *dt_smallinteger_u;             SQLLEN *ptr_smallinteger_u;
SQLCHAR             *dt_integer_s;                  SQLLEN *ptr_integer_s;
SQLCHAR             *dt_integer_u;                  SQLLEN *ptr_integer_u;            
SQLCHAR             *dt_largeint;                   SQLLEN *ptr_largeint;
SQLCHAR             *dt_real;                       SQLLEN *ptr_real;
SQLCHAR             *dt_float;                      SQLLEN *ptr_float;
SQLCHAR             *dt_double_precision;           SQLLEN *ptr_double_precision;
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
SQLCHAR             *dt_bignum_s;                   SQLLEN *ptr_bignum_s;
SQLCHAR             *dt_bignum_u;                   SQLLEN *ptr_bignum_u;

// Global Variables.
SQLHANDLE  handle[ 5 ];    // 0 = nothing, 1 = environment 2 = connection 3 = statement 4 = used for DELETE and UPDATE
char      *datasource;     // Datasource name to make the ODBC connection through.
char      *uid;            // User identification to run the tests as.
char      *password;       // User identification password.
char      *machine = "local";// Storing which platform is running from
bool      debug = false;   // Print out debug info
int       errorChecking = STANDARD;   // Error checking type.
int       failureInjectionCount;
int       goodRowCount;
SQLCHAR   dataCQD[ 512 ];		//This is for CQD checking

// Post rowset execution analysis. This allows us to check the statuses of the rows we inserted.
SQLUSMALLINT *rowsetStatusArray; // Array showing the status of each row after running SQLExecute().
SQLUSMALLINT *expectedRowsetStatusArray; // Expected Array showing the status of each row after running SQLExecute().
SQLUSMALLINT *rowsetOperationArray; // Array showing which rows to process when running SQLExecute().
SQLULEN       rowsProcessed;     // The number of rows processed after running SQLExecute().
table_rowset *rowset;  // Where we will store the data prior to inserting it into the database.

// Timing metrics
bool  timeMetrics = false; // Display time metrics information. 
char logfilename[256];

// SK - for ALM log
/****************************************************************
** Local variables for ALM
****************************************************************/
time_t	ALM_Test_start, ALM_Test_end;
char		ALM_log_file_buff[1024];
char		Heading[MAX_STRING_SIZE];
char		ALM_NextTestInfo[MAX_STRING_SIZE];
char		ALM_TestCaseId[12];   
typedef enum PassFail {PASSED, FAILED} PassFail;
PassFail _TestCase;
// End for ALM log


// Function Definitions.
/* For ALM Formatted Log output */
void ALM_LogTestCaseInfo(char *, char *, int, int);
void ALM_LogTestResultInfo(PassFail, time_t, time_t);
void ALM_TestInformation(char *);
/* End  For ALM Formatted Log output */

bool NextTest( void );
bool IgnoreTest( void );
bool EstablishHandlesAndConnection( void );
bool CreateTable( void );
void IgnoreMsg( SQLCHAR *state, SDWORD nativeError );
bool ShouldIgnoreMsg( SQLCHAR *state, SDWORD nativeError );
void ClearIgnore( void );
int  CheckMsgs( char* sqlFunction, int lineNumber );
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
char* Param_Status_Ptr( SQLUSMALLINT parameter_status );
void DisplayTimeMetrics( void );
void RecordToLog( char* format, ... );
char* CheckForCQD( char *CQD );
int TestByteOrder(void);
bool BindParametersA( int bindOrientations, int actions, int injectionTypes );

int TestByteOrder(void)
{
    short int word = 0x0001;
    char *byte = (char *) &word;
    return(byte[0] ? LITTLEENDIAN : BIGENDIAN);
}

char * __itoa(int n, char *buff, int base) {

   char t[100], *c=t, *f=buff;
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

int int_to_ucs2 (int intVal, char *usc2_array) {
	int i=0, j=0;
	char buffer[STRINGMAXDBL];

	__itoa (intVal,buffer,10);
	for (i=0; i<(int)strlen(buffer); i++) {
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

bool array_cmp(char *arr1, char *arr2, int size) {
	for (int i=0; i<size; i++) {
		if (arr1[i] != arr2[i]) return 1;
	}

	return 0;
}

/* Function          : Param_Status_Str
   Calling Arguments : int : The parameter status definition
   Return Arguments  : char* : The C string representing the parameter status

   Description: 
   This returns the parameter status definition C string.
*/

char* Param_Status_Ptr( SQLUSMALLINT parameter_status )
{
    switch( parameter_status )
    {
        case SQL_PARAM_SUCCESS:
            return( "SQL_PARAM_SUCCESS" );
        case SQL_PARAM_SUCCESS_WITH_INFO:
             return( "SQL_PARAM_SUCCESS_WITH_INFO" );
        case SQL_PARAM_ERROR:
             return( "SQL_PARAM_ERROR" );
        case SQL_PARAM_UNUSED:
             return( "SQL_PARAM_UNUSED" );
        case SQL_PARAM_DIAG_UNAVAILABLE:
             return( "SQL_PARAM_DIAG_UNAVAILABLE" );
        default:
            return( "UNKNOWN" );
    }
    return( "INTERNAL ERROR: Param_Status_Ptr( )" );
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
   Calling Arguments : char* : vfwRecordToLog() format string.
                       ...   : arguments for formated string.
   Return Arguments  : void

   Description: 
   Writes the message to a log file.
*/

void RecordToLog( char* format, ... )
{
    FILE *logFilePtr;
    time_t wall_clock;
    char date[ 100 ];
	int ret;

	logFilePtr = fopen( logfilename, "a" );
    if( logFilePtr == NULL ) 
    {
        // TODO: Debugging
    }

    va_list ArgumentList;
    if( logFilePtr != (FILE*)NULL )
    {
		if (debug) {
			wall_clock = time( NULL );
			strftime( date, 100, "%Y %b %d %H:%M:%S", localtime( &wall_clock ) );
			if( fprintf( logFilePtr, "[%s] ", date ) == -1 )
			{
				// TODO: Debugging
			}
		}

        va_start( ArgumentList, format );
        vprintf( format, ArgumentList );
		va_end(ArgumentList);

        va_start( ArgumentList, format );
        ret = vfprintf( logFilePtr, format, ArgumentList );
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
   Calling Arguments : char* : vfwRecordToLog() format string.
                       ...   : arguments for formated string.
   Return Arguments  : void

   Description: 
   Writes the message to the ALM log file with ALM format.
*/
void RecordTo_ALM_Log( char* format, ... )
{
    FILE *ALM_logFilePtr;
    time_t wall_clock;
    char date[ 100 ];
	int ret;

	ALM_logFilePtr = fopen( ALM_log_file_buff, "a" );
    if( ALM_logFilePtr == NULL ) 
    {
        // TODO: Debugging
    }

    va_list ArgumentList;
    if( ALM_logFilePtr != (FILE*)NULL )
    {
		if (debug) {
			wall_clock = time( NULL );
			strftime( date, 100, "%Y %b %d %H:%M:%S", localtime( &wall_clock ) );
			if( fprintf( ALM_logFilePtr, "[%s] ", date ) == -1 )
			{
				// TODO: Debugging
			}
		}

//      va_start( ArgumentList, format );
//      vprintf( format, ArgumentList );
//      va_end(ArgumentList);

        va_start( ArgumentList, format );
        ret = vfprintf( ALM_logFilePtr, format, ArgumentList );
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
   Calling Arguments : char* : CQD that is being looked for.
   Return Arguments  : char* : CQD value. An empty string is returned if 
                               nothing is retrieved.

   Description: 
   This looks for a CQD and thn returns the CQD value.
*/
char* CheckForCQD( char *CQD )
{
    SQLRETURN  retcode;       // Used to gather the return value of all ODBC API calls.
    // We need to check _ALL_ CQD's on the system. So we make sure we can see the ones not
    // exposed to the customer too.
    while( (retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)"CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'ON' ", SQL_NTS ) ) == SQL_STILL_EXECUTING );
    if( retcode != SQL_SUCCESS )
    {
        CheckMsgs( "SQLExecDirect()", __LINE__ );
        retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( "SQLFreeStmt()", __LINE__ );
        }
	    while( (retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)"CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'OFF' ", SQL_NTS ) ) == SQL_STILL_EXECUTING );
        return " " ;
    }

    // Execute the command to request information about the CQD.
    char *SQLCommand;
    SQLCommand = (char *)malloc( strlen( CQD ) + 21 ); // The 21 is for "SHOWCONTROL DEFAULT " and a null.
    sprintf( SQLCommand, "SHOWCONTROL DEFAULT %s", CQD );
    while( ( retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ],(SQLCHAR*)SQLCommand, SQL_NTS ) ) == SQL_STILL_EXECUTING );
    free( SQLCommand );
    if( retcode != SQL_SUCCESS )
    {
        CheckMsgs( "SQLExecDirect()", __LINE__ );
        retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( "SQLFreeStmt()", __LINE__ );
        }
	    while( (retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)"CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'OFF' ", SQL_NTS ) ) == SQL_STILL_EXECUTING );
        return " " ;
    }

    // Now we fetch the data if there is any.
    SQLLEN dataPtr;
    dataPtr = SQL_NTS;
    retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 1, SQL_C_CHAR, (SQLPOINTER) dataCQD, 512, &dataPtr );
    if( retcode != SQL_SUCCESS )
    {
        CheckMsgs( "SQLBindCol()", __LINE__ );
        retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
        if( retcode != SQL_SUCCESS )    
        {
            CheckMsgs( "SQLFreeStmt()", __LINE__ );
        }
	    while( (retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)"CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'OFF' ", SQL_NTS ) ) == SQL_STILL_EXECUTING );
        return " " ;
    }

    char *pointer;
    while( true )
    {
		while( ( retcode = SQLFetch( handle[ SQL_HANDLE_STMT ] ) ) == SQL_STILL_EXECUTING );
		if( retcode == SQL_SUCCESS || retcode == SQL_SUCCESS_WITH_INFO )
        {
            pointer = strstr( (char*)dataCQD, CQD );
            if( pointer != NULL )
            {
                // Move past the CQD name.
                pointer += (int)strlen( CQD );
                // Move past white spacing.
                while( ( ( *pointer == ' ' ) || ( *pointer == '\t' ) ) && ( *pointer != '\0' ) )
                {
                    pointer++;
                }
                retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
                if( retcode != SQL_SUCCESS )    
                {
                    CheckMsgs( "SQLFreeStmt()", __LINE__ );
                }
			   while( (retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)"CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'OFF' ", SQL_NTS ) ) == SQL_STILL_EXECUTING );
               return pointer;
            }
        }
        else
        {
            break;
        }
	}

     retcode = SQLFreeStmt( handle[ SQL_HANDLE_STMT ], SQL_CLOSE ); // Free and clearup the statement handle.
    if( retcode != SQL_SUCCESS )    
    {
        CheckMsgs( "SQLFreeStmt()", __LINE__ );
    }
   while( (retcode = SQLExecDirect( handle[ SQL_HANDLE_STMT ], (SQLCHAR*)"CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'OFF' ", SQL_NTS ) ) == SQL_STILL_EXECUTING );
    return " ";
}

void DisplayRowsets(int bindOrientations, int rowsetPos) {
    switch( bindOrientations )
    {
        case ROW:
        case SINGLE:
		if (rowset[ rowsetPos ].dt_integer_s[0] != '\0')
			RecordToLog( "[%s] %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %d %s %s\n", 
				(char*)rowset[ rowsetPos ].dt_largeint,
				(char*)rowset[ rowsetPos ].dt_char_iso,
				(char*)rowset[ rowsetPos ].dt_char_ucs,
				(char*)rowset[ rowsetPos ].dt_varchar_iso,
				(char*)rowset[ rowsetPos ].dt_varchar_ucs,
				(char*)rowset[ rowsetPos ].dt_longvarchar_iso,
				(char*)rowset[ rowsetPos ].dt_longvarchar_ucs,
				(char*)rowset[ rowsetPos ].dt_nchar,
				(char*)rowset[ rowsetPos ].dt_ncharvarying,
				(char*)rowset[ rowsetPos ].dt_decimal_s,
				(char*)rowset[ rowsetPos ].dt_decimal_u,
				(char*)rowset[ rowsetPos ].dt_numeric_s,
				(char*)rowset[ rowsetPos ].dt_numeric_u,
				(char*)rowset[ rowsetPos ].dt_tinyint_s,
				(char*)rowset[ rowsetPos ].dt_tinyint_u,
				(char*)rowset[ rowsetPos ].dt_smallinteger_s,
				(char*)rowset[ rowsetPos ].dt_smallinteger_u,
 				(char*)rowset[ rowsetPos ].dt_integer_s,
				(char*)rowset[ rowsetPos ].dt_integer_u,
				(char*)rowset[ rowsetPos ].dt_real,
				(char*)rowset[ rowsetPos ].dt_float,
				(char*)rowset[ rowsetPos ].dt_double_precision,
				rowset[ rowsetPos ].dt_timestamp.day,
				(char*)rowset[ rowsetPos ].dt_bignum_s,
				(char*)rowset[ rowsetPos ].dt_bignum_u
			);
		else
			RecordToLog( "[%s] %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s null %s %s %s %s %s %d %s %s\n", 
				(char*)rowset[ rowsetPos ].dt_largeint,
				(char*)rowset[ rowsetPos ].dt_char_iso,
				(char*)rowset[ rowsetPos ].dt_char_ucs,
				(char*)rowset[ rowsetPos ].dt_varchar_iso,
				(char*)rowset[ rowsetPos ].dt_varchar_ucs,
				(char*)rowset[ rowsetPos ].dt_longvarchar_iso,
				(char*)rowset[ rowsetPos ].dt_longvarchar_ucs,
				(char*)rowset[ rowsetPos ].dt_nchar,
				(char*)rowset[ rowsetPos ].dt_ncharvarying,
				(char*)rowset[ rowsetPos ].dt_decimal_s,
				(char*)rowset[ rowsetPos ].dt_decimal_u,
				(char*)rowset[ rowsetPos ].dt_numeric_s,
				(char*)rowset[ rowsetPos ].dt_numeric_u,
				(char*)rowset[ rowsetPos ].dt_tinyint_s,
				(char*)rowset[ rowsetPos ].dt_tinyint_u,
				(char*)rowset[ rowsetPos ].dt_smallinteger_s,
				(char*)rowset[ rowsetPos ].dt_smallinteger_u,
 				//(char*)rowset[ rowsetPos ].dt_integer_s,
				(char*)rowset[ rowsetPos ].dt_integer_u,
				(char*)rowset[ rowsetPos ].dt_real,
				(char*)rowset[ rowsetPos ].dt_float,
				(char*)rowset[ rowsetPos ].dt_double_precision,
				rowset[ rowsetPos ].dt_timestamp.day,
				(char*)rowset[ rowsetPos ].dt_bignum_s,
				(char*)rowset[ rowsetPos ].dt_bignum_u
			);
            break;
        case COLUMN:
		if (dt_integer_s[ rowsetPos * STRINGMAX  ] != '\0')
			RecordToLog( "[%s] %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %d %s %s\n", 
            			(char*)&dt_largeint[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_char_iso[ rowsetPos * STRINGMAX ],
            			(char*)&dt_char_ucs[ rowsetPos * STRINGMAXDBL  ],
            			(char*)&dt_varchar_iso[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_varchar_ucs[ rowsetPos * STRINGMAXDBL  ],
            			(char*)&dt_longvarchar_iso[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_longvarchar_ucs[ rowsetPos * STRINGMAXDBL  ],            
            			(char*)&dt_nchar[ rowsetPos * STRINGMAXDBL  ],
            			(char*)&dt_ncharvarying[ rowsetPos * STRINGMAXDBL  ],
            			(char*)&dt_decimal_s[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_decimal_u[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_numeric_s[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_numeric_u[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_tinyint_s[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_tinyint_u[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_smallinteger_s[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_smallinteger_u[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_integer_s[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_integer_u[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_real[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_float[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_double_precision[ rowsetPos * STRINGMAX  ],
						dt_timestamp[ rowsetPos ].day,
            			(char*)&dt_bignum_s[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_bignum_u[ rowsetPos * STRINGMAX  ]
			);
		else
			RecordToLog( "[%s] %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s null %s %s %s %s %s %d %s %s\n", 
            			(char*)&dt_largeint[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_char_iso[ rowsetPos * STRINGMAX ],
            			(char*)&dt_char_ucs[ rowsetPos * STRINGMAXDBL  ],
            			(char*)&dt_varchar_iso[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_varchar_ucs[ rowsetPos * STRINGMAXDBL  ],
            			(char*)&dt_longvarchar_iso[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_longvarchar_ucs[ rowsetPos * STRINGMAXDBL  ],            
            			(char*)&dt_nchar[ rowsetPos * STRINGMAXDBL  ],
            			(char*)&dt_ncharvarying[ rowsetPos * STRINGMAXDBL  ],
            			(char*)&dt_decimal_s[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_decimal_u[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_numeric_s[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_numeric_u[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_tinyint_s[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_tinyint_u[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_smallinteger_s[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_smallinteger_u[ rowsetPos * STRINGMAX  ],
            			//(char*)&dt_integer_s[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_integer_u[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_real[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_float[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_double_precision[ rowsetPos * STRINGMAX  ],
                        dt_timestamp[ rowsetPos ].day,
            			(char*)&dt_bignum_s[ rowsetPos * STRINGMAX  ],
            			(char*)&dt_bignum_u[ rowsetPos * STRINGMAX  ]
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
                dt_char_iso = (SQLCHAR *) malloc( rowsetSizes * STRINGMAX);
                ptr_char_iso = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_char_ucs = (SQLCHAR *) malloc( rowsetSizes * STRINGMAXDBL);
                ptr_char_ucs = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_varchar_iso = (SQLCHAR *) malloc( rowsetSizes * STRINGMAX);
                ptr_varchar_iso = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_varchar_ucs = (SQLCHAR *) malloc( rowsetSizes * STRINGMAXDBL);
                ptr_varchar_ucs = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_longvarchar_iso = (SQLCHAR *) malloc( rowsetSizes * STRINGMAX);
                ptr_longvarchar_iso = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_longvarchar_ucs = (SQLCHAR *) malloc( rowsetSizes * STRINGMAXDBL);
                ptr_longvarchar_ucs = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_nchar = (SQLCHAR *) malloc( rowsetSizes * STRINGMAXDBL );
                ptr_nchar = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_ncharvarying = (SQLCHAR *) malloc( rowsetSizes * STRINGMAXDBL );
                ptr_ncharvarying = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_decimal_s = (SQLCHAR *) malloc( rowsetSizes * STRINGMAX);
                ptr_decimal_s = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_decimal_u = (SQLCHAR *) malloc( rowsetSizes * STRINGMAX);
                ptr_decimal_u = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_numeric_s = (SQLCHAR *) malloc( rowsetSizes * STRINGMAX);
                ptr_numeric_s = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_numeric_u = (SQLCHAR *) malloc( rowsetSizes * STRINGMAX);
                ptr_numeric_u = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_tinyint_s = (SQLCHAR *) malloc( rowsetSizes * STRINGMAX );
                ptr_tinyint_s = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_tinyint_u = (SQLCHAR *) malloc( rowsetSizes * STRINGMAX );
                ptr_tinyint_u = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_smallinteger_s = (SQLCHAR *) malloc( rowsetSizes * STRINGMAX );
                ptr_smallinteger_s = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_smallinteger_u = (SQLCHAR *) malloc( rowsetSizes * STRINGMAX );
                ptr_smallinteger_u = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_integer_s = (SQLCHAR *) malloc( rowsetSizes * STRINGMAX );
                ptr_integer_s = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_integer_u = (SQLCHAR *) malloc( rowsetSizes * STRINGMAX );
                ptr_integer_u = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_largeint = (SQLCHAR *) malloc( rowsetSizes * STRINGMAX );
                ptr_largeint = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_real = (SQLCHAR *) malloc( rowsetSizes * STRINGMAX );
                ptr_real = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_float = (SQLCHAR *) malloc( rowsetSizes * STRINGMAX );
                ptr_float = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_double_precision = (SQLCHAR *) malloc( rowsetSizes * STRINGMAX );
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
                dt_bignum_s = (SQLCHAR *) malloc( rowsetSizes * STRINGMAX);
                ptr_bignum_s = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );
                dt_bignum_u = (SQLCHAR *) malloc( rowsetSizes * STRINGMAX);
                ptr_bignum_u = (SQLLEN*)malloc( rowsetSizes * sizeof( SQLLEN ) );

				memset(dt_char_iso , 0, rowsetSizes *   STRINGMAX);
                memset(ptr_char_iso , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_char_ucs , 0, rowsetSizes *   STRINGMAXDBL);
                memset(ptr_char_ucs , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_varchar_iso , 0, rowsetSizes *   STRINGMAX);
                memset(ptr_varchar_iso , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_varchar_ucs , 0, rowsetSizes *   STRINGMAXDBL);
                memset(ptr_varchar_ucs , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_longvarchar_iso , 0, rowsetSizes *   STRINGMAX);
                memset(ptr_longvarchar_iso , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_longvarchar_ucs , 0, rowsetSizes *   STRINGMAXDBL);
                memset(ptr_longvarchar_ucs , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_nchar , 0, rowsetSizes *   STRINGMAXDBL );
                memset(ptr_nchar , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_ncharvarying , 0, rowsetSizes *   STRINGMAXDBL );
                memset(ptr_ncharvarying , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_decimal_s , 0, rowsetSizes *   STRINGMAX);
                memset(ptr_decimal_s , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_decimal_u ,0,  rowsetSizes *   STRINGMAX);
                memset(ptr_decimal_u , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_numeric_s , 0, rowsetSizes *   STRINGMAX);
                memset(ptr_numeric_s , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_numeric_u , 0, rowsetSizes *   STRINGMAX);
                memset(ptr_numeric_u , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_tinyint_s , 0, rowsetSizes *   STRINGMAX );
                memset(ptr_tinyint_s , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_tinyint_u , 0, rowsetSizes *   STRINGMAX );
                memset(ptr_tinyint_u , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_smallinteger_s , 0, rowsetSizes *   STRINGMAX );
                memset(ptr_smallinteger_s , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_smallinteger_u , 0, rowsetSizes *   STRINGMAX );
                memset(ptr_smallinteger_u , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_integer_s , 0, rowsetSizes *   STRINGMAX );
                memset(ptr_integer_s , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_integer_u , 0, rowsetSizes *   STRINGMAX );
                memset(ptr_integer_u , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_largeint , 0, rowsetSizes *   STRINGMAX );
                memset(ptr_largeint , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_real , 0, rowsetSizes *   STRINGMAX );
                memset(ptr_real , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_float , 0, rowsetSizes *   STRINGMAX );
                memset(ptr_float , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_double_precision , 0, rowsetSizes *   STRINGMAX );
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
                memset(dt_bignum_s , 0, rowsetSizes *   STRINGMAX);
                memset(ptr_bignum_s , 0, rowsetSizes *   sizeof( SQLLEN ) );
                memset(dt_bignum_u , 0, rowsetSizes *   STRINGMAX);
                memset(ptr_bignum_u , 0, rowsetSizes *   sizeof( SQLLEN ) );
			}
            else
            {
                dt_char_iso = (SQLCHAR *) malloc( 1 * STRINGMAX);
                ptr_char_iso = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_char_ucs = (SQLCHAR *) malloc( 1 * STRINGMAXDBL);
                ptr_char_ucs = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_varchar_iso = (SQLCHAR *) malloc( 1 * STRINGMAX);
                ptr_varchar_iso = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_varchar_ucs = (SQLCHAR *) malloc( 1 * STRINGMAXDBL);
                ptr_varchar_ucs = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_longvarchar_iso = (SQLCHAR *) malloc( 1 * STRINGMAX);
                ptr_longvarchar_iso = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_longvarchar_ucs = (SQLCHAR *) malloc( 1 * STRINGMAXDBL);
                ptr_longvarchar_ucs = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_nchar = (SQLCHAR *) malloc( 1 * STRINGMAXDBL );
                ptr_nchar = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_ncharvarying = (SQLCHAR *) malloc( 1 * STRINGMAXDBL );
                ptr_ncharvarying = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_decimal_s = (SQLCHAR *) malloc( 1 * STRINGMAX);
                ptr_decimal_s = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_decimal_u = (SQLCHAR *) malloc( 1 * STRINGMAX);
                ptr_decimal_u = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_numeric_s = (SQLCHAR *) malloc( 1 * STRINGMAX);
                ptr_numeric_s = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_numeric_u = (SQLCHAR *) malloc( 1 * STRINGMAX);
                ptr_numeric_u = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_tinyint_s = (SQLCHAR *) malloc( 1 * STRINGMAX );
                ptr_tinyint_s = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_tinyint_u = (SQLCHAR *) malloc( 1 * STRINGMAX );
                ptr_tinyint_u = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_smallinteger_s = (SQLCHAR *) malloc( 1 * STRINGMAX );
                ptr_smallinteger_s = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_smallinteger_u = (SQLCHAR *) malloc( 1 * STRINGMAX );
                ptr_smallinteger_u = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_integer_s = (SQLCHAR *) malloc( 1 * STRINGMAX );
                ptr_integer_s = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_integer_u = (SQLCHAR *) malloc( 1 * STRINGMAX );
                ptr_integer_u = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_largeint = (SQLCHAR *) malloc( 1 * STRINGMAX );
                ptr_largeint = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_real = (SQLCHAR *) malloc( 1 * STRINGMAX );
                ptr_real = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_float = (SQLCHAR *) malloc( 1 * STRINGMAX );
                ptr_float = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_double_precision = (SQLCHAR *) malloc( 1 * STRINGMAX );
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
                dt_bignum_s = (SQLCHAR *) malloc( 1 * STRINGMAX);
                ptr_bignum_s = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );
                dt_bignum_u = (SQLCHAR *) malloc( 1 * STRINGMAX);
                ptr_bignum_u = (SQLLEN*)malloc( 1 * sizeof( SQLLEN ) );

				memset(dt_char_iso ,   0, STRINGMAX);
                memset(ptr_char_iso ,   0, sizeof( SQLLEN ) );
                memset(dt_char_ucs ,   0, STRINGMAXDBL);
                memset(ptr_char_ucs ,   0, sizeof( SQLLEN ) );
                memset(dt_varchar_iso ,  0,  STRINGMAX);
                memset(ptr_varchar_iso , 0,   sizeof( SQLLEN ) );
                memset(dt_varchar_ucs ,  0,  STRINGMAXDBL);
                memset(ptr_varchar_ucs , 0,   sizeof( SQLLEN ) );
                memset(dt_longvarchar_iso , 0,   STRINGMAX);
                memset(ptr_longvarchar_iso ,0,    sizeof( SQLLEN ) );
                memset(dt_longvarchar_ucs , 0,   STRINGMAXDBL);
                memset(ptr_longvarchar_ucs ,0,    sizeof( SQLLEN ) );
                memset(dt_nchar , 0,   STRINGMAXDBL );
                memset(ptr_nchar , 0,   sizeof( SQLLEN ) );
                memset(dt_ncharvarying , 0,   STRINGMAXDBL );
                memset(ptr_ncharvarying , 0,   sizeof( SQLLEN ) );
                memset(dt_decimal_s , 0,   STRINGMAX);
                memset(ptr_decimal_s ,0,    sizeof( SQLLEN ) );
                memset(dt_decimal_u , 0,   STRINGMAX);
                memset(ptr_decimal_u ,0,    sizeof( SQLLEN ) );
                memset(dt_numeric_s , 0,   STRINGMAX);
                memset(ptr_numeric_s , 0,   sizeof( SQLLEN ) );
                memset(dt_numeric_u , 0,   STRINGMAX);
                memset(ptr_numeric_u ,0,    sizeof( SQLLEN ) );
                memset(dt_tinyint_s , 0,   STRINGMAX );
                memset(ptr_tinyint_s ,0,    sizeof( SQLLEN ) );
                memset(dt_tinyint_u , 0,   STRINGMAX );
                memset(ptr_tinyint_u ,0,    sizeof( SQLLEN ) );
                memset(dt_smallinteger_s ,0,    STRINGMAX );
                memset(ptr_smallinteger_s ,0,    sizeof( SQLLEN ) );
                memset(dt_smallinteger_u ,0,    STRINGMAX );
                memset(ptr_smallinteger_u ,0,    sizeof( SQLLEN ) );
                memset(dt_integer_s ,0,    STRINGMAX );
                memset(ptr_integer_s ,0,    sizeof( SQLLEN ) );
                memset(dt_integer_u , 0,   STRINGMAX );
                memset(ptr_integer_u , 0,   sizeof( SQLLEN ) );
                memset(dt_largeint , 0,   STRINGMAX );
                memset(ptr_largeint , 0,   sizeof( SQLLEN ) );
                memset(dt_real ,0,    STRINGMAX );
                memset(ptr_real , 0,   sizeof( SQLLEN ) );
                memset(dt_float , 0,   STRINGMAX );
                memset(ptr_float ,0,    sizeof( SQLLEN ) );
                memset(dt_double_precision ,0,    STRINGMAX );
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
                memset(dt_bignum_s , 0,   STRINGMAX);
                memset(ptr_bignum_s , 0,   sizeof( SQLLEN ) );
                memset(dt_bignum_u , 0,   STRINGMAX);
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
                rowset[ loop ].ptr_char_iso = SQL_NTS;
                rowset[ loop ].ptr_char_ucs = SQL_NTS;
                rowset[ loop ].ptr_varchar_iso = SQL_NTS;
                rowset[ loop ].ptr_varchar_ucs = SQL_NTS;
                rowset[ loop ].ptr_longvarchar_iso = SQL_NTS;
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
			free( rowset ); // <---Got to love row-wise rowsets!
            break;
        case COLUMN:
            free( dt_char_iso );                  free( ptr_char_iso );
            free( dt_char_ucs );                  free( ptr_char_ucs );
            free( dt_varchar_iso );               free( ptr_varchar_iso );
            free( dt_varchar_ucs );               free( ptr_varchar_ucs );
            free( dt_longvarchar_iso );           free( ptr_longvarchar_iso );
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
                retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], 2, SQL_PARAM_INPUT, SQL_C_CHAR,
                                            SQL_BIGINT, 0, 0,
                                            (SQLPOINTER) rowset[ 0 ].dt_largeint, STRINGMAX ,
                                            &rowset[ 0 ].ptr_largeint );
                if( retcode != SQL_SUCCESS )
                {
                    CheckMsgs( "SQLBindParameter()", __LINE__ );
                    FreeRowsets( bindOrientations );
                    return false;
                }
                break;
            }

            // Here is where we now bind the C variables to the table columns.
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 1, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_CHAR, STRINGMAX - 1, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_char_iso, STRINGMAX - 1 ,
                                        &rowset[ 0 ].ptr_char_iso );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 2, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_CHAR, STRINGMAXDBL, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_char_ucs, STRINGMAXDBL ,
                                        &rowset[ 0 ].ptr_char_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 3, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_VARCHAR, STRINGMAX, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_varchar_iso, STRINGMAX ,
                                        &rowset[ 0 ].ptr_varchar_iso );                                        
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 4, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_VARCHAR, STRINGMAXDBL, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_varchar_ucs, STRINGMAXDBL ,
                                        &rowset[ 0 ].ptr_varchar_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 5, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_LONGVARCHAR, STRINGMAX, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_longvarchar_iso, STRINGMAX ,
                                        &rowset[ 0 ].ptr_longvarchar_iso );                                        
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 6, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_LONGVARCHAR, STRINGMAXDBL, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_longvarchar_ucs, STRINGMAXDBL ,
                                        &rowset[ 0 ].ptr_longvarchar_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 7, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_WCHAR, STRINGMAXDBL, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_nchar, STRINGMAXDBL,
                                        &rowset[ 0 ].ptr_nchar );                                        
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 8, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_WVARCHAR, STRINGMAXDBL, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_ncharvarying, STRINGMAXDBL,
                                        &rowset[ 0 ].ptr_ncharvarying );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 9, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_DECIMAL, 8, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_decimal_s, STRINGMAX ,
                                        &rowset[ 0 ].ptr_decimal_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 10, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_DECIMAL, 8, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_decimal_u, STRINGMAX ,
                                        &rowset[ 0 ].ptr_decimal_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 11, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_NUMERIC, 8, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_numeric_s, STRINGMAX ,
                                        &rowset[ 0 ].ptr_numeric_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 12, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_NUMERIC, 8, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_numeric_u, STRINGMAX ,
                                        &rowset[ 0 ].ptr_numeric_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 13, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_TINYINT, 0, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_tinyint_s, STRINGMAX ,
                                        &rowset[ 0 ].ptr_tinyint_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 14, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_TINYINT, 0, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_tinyint_u, STRINGMAX ,
                                        &rowset[ 0 ].ptr_tinyint_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                        
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 15, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_SMALLINT, 0, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_smallinteger_s, STRINGMAX ,
                                        &rowset[ 0 ].ptr_smallinteger_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 16, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_SMALLINT, 0, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_smallinteger_u, STRINGMAX ,
                                        &rowset[ 0 ].ptr_smallinteger_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                                             
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 17, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_INTEGER, 0, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_integer_s, STRINGMAX ,
                                        &rowset[ 0 ].ptr_integer_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                        
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 18, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_INTEGER, 0, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_integer_u, STRINGMAX ,
                                        &rowset[ 0 ].ptr_integer_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
            
			if( actions == UPDATE ) {
				offset = -1;
			}
			else {
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 19, SQL_PARAM_INPUT, SQL_C_CHAR,
											SQL_BIGINT, 0, 0,
											(SQLPOINTER) rowset[ 0 ].dt_largeint, STRINGMAX ,
											&rowset[ 0 ].ptr_largeint );
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( "SQLBindParameter()", __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}
			}
                     
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 20, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_REAL, 0, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_real, STRINGMAX ,
                                        &rowset[ 0 ].ptr_real );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 21, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_FLOAT, 0, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_float, STRINGMAX ,
                                        &rowset[ 0 ].ptr_float );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                        
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 22, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_DOUBLE, 0, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_double_precision, STRINGMAX ,
                                        &rowset[ 0 ].ptr_double_precision );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }

            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 23, SQL_PARAM_INPUT, SQL_C_TYPE_DATE ,
                                        SQL_TYPE_DATE, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_date, 0,
                                        &rowset[ 0 ].ptr_date );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 24, SQL_PARAM_INPUT, SQL_C_TYPE_TIME ,
                                        SQL_TYPE_TIME, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_time, 0,
                                        &rowset[ 0 ].ptr_time );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 25, SQL_PARAM_INPUT, SQL_C_TYPE_TIMESTAMP ,
                                        SQL_TYPE_TIMESTAMP, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_timestamp, 0,
                                        &rowset[ 0 ].ptr_timestamp );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 26, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_YEAR, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_year,0,
                                        &rowset[ 0 ].ptr_interval_year );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 27, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_MONTH, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_month, 0,
                                        &rowset[ 0 ].ptr_interval_month );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 28, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_DAY, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_day, 0,
                                        &rowset[ 0 ].ptr_interval_day );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 29, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_HOUR, 5, 0,     
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_hour, 0,
                                        &rowset[ 0 ].ptr_interval_hour );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 30, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_MINUTE, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_minute, 0,
                                        &rowset[ 0 ].ptr_interval_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 31, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_SECOND, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_second, 0,
                                        &rowset[ 0 ].ptr_interval_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 32, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_YEAR_TO_MONTH, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_year_to_month, 0,
                                        &rowset[ 0 ].ptr_interval_year_to_month );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 33, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_DAY_TO_HOUR, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_day_to_hour, 0,
                                        &rowset[ 0 ].ptr_interval_day_to_hour );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 34, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_DAY_TO_MINUTE, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_day_to_minute, 0,
                                        &rowset[ 0 ].ptr_interval_day_to_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 35, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_DAY_TO_SECOND, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_day_to_second, 0,
                                        &rowset[ 0 ].ptr_interval_day_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 36, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_HOUR_TO_MINUTE, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_hour_to_minute, 0,
                                        &rowset[ 0 ].ptr_interval_hour_to_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 37, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_HOUR_TO_SECOND, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_hour_to_second, 0,
                                        &rowset[ 0 ].ptr_interval_hour_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 38, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_MINUTE_TO_SECOND, 5, 0, 
                                        (SQLPOINTER) &rowset[ 0 ].dt_interval_minute_to_second, 0,
                                        &rowset[ 0 ].ptr_interval_minute_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
           
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 39, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_NUMERIC, 19, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_bignum_s, STRINGMAX ,
                                        &rowset[ 0 ].ptr_bignum_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 40, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_NUMERIC, 19, 0,
                                        (SQLPOINTER) rowset[ 0 ].dt_bignum_u, STRINGMAX ,
                                        &rowset[ 0 ].ptr_bignum_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }

			if( actions == UPDATE ) {
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], 40, SQL_PARAM_INPUT, SQL_C_CHAR,
											SQL_BIGINT, 0, 0,
											(SQLPOINTER) rowset[ 0 ].dt_largeint, STRINGMAX ,
											&rowset[ 0 ].ptr_largeint );
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( "SQLBindParameter()", __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}
			}

			break;

        case COLUMN:
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 1, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_CHAR, STRINGMAX, 0,
                                        (SQLPOINTER) dt_char_iso, STRINGMAX ,
                                        ptr_char_iso );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 2, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_CHAR, STRINGMAXDBL, 0,
                                        (SQLPOINTER) dt_char_ucs, STRINGMAXDBL ,
                                        ptr_char_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 3, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_VARCHAR, STRINGMAX, 0,
                                        (SQLPOINTER) dt_varchar_iso, STRINGMAX ,
                                        ptr_varchar_iso );                                        
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 4, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_VARCHAR, STRINGMAXDBL, 0,
                                        (SQLPOINTER) dt_varchar_ucs, STRINGMAXDBL ,
                                        ptr_varchar_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 5, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_LONGVARCHAR, STRINGMAX, 0,
                                        (SQLPOINTER) dt_longvarchar_iso, STRINGMAX ,
                                        ptr_longvarchar_iso );                                        
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 6, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_LONGVARCHAR, STRINGMAXDBL, 0,
                                        (SQLPOINTER) dt_longvarchar_ucs, STRINGMAXDBL ,
                                        ptr_longvarchar_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 7, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_WCHAR, STRINGMAXDBL, 0,
                                        (SQLPOINTER) dt_nchar, STRINGMAXDBL,
                                        ptr_nchar );                                        
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 8, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_WVARCHAR, STRINGMAXDBL, 0,
                                        (SQLPOINTER) dt_ncharvarying, STRINGMAXDBL,
                                        ptr_ncharvarying );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 9, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_DECIMAL, 8, 0,
                                        (SQLPOINTER) dt_decimal_s, STRINGMAX ,
                                        ptr_decimal_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 10, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_DECIMAL, 8, 0,
                                        (SQLPOINTER) dt_decimal_u, STRINGMAX ,
                                        ptr_decimal_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 11, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_NUMERIC, 8, 0,
                                        (SQLPOINTER) dt_numeric_s, STRINGMAX ,
                                        ptr_numeric_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 12, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_NUMERIC, 8, 0,
                                        (SQLPOINTER) dt_numeric_u, STRINGMAX ,
                                        ptr_numeric_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 13, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_TINYINT, 0, 0,
                                        (SQLPOINTER) dt_tinyint_s, STRINGMAX ,
                                        ptr_tinyint_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 14, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_TINYINT, 0, 0,
                                        (SQLPOINTER) dt_tinyint_u, STRINGMAX ,
                                        ptr_tinyint_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                        
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 15, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_SMALLINT, 0, 0,
                                        (SQLPOINTER) dt_smallinteger_s, STRINGMAX ,
                                        ptr_smallinteger_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 16, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_SMALLINT, 0, 0,
                                        (SQLPOINTER) dt_smallinteger_u, STRINGMAX ,
                                        ptr_smallinteger_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                                             
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 17, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_INTEGER, 0, 0,
                                        (SQLPOINTER) dt_integer_s, STRINGMAX ,
                                        ptr_integer_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                        
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 18, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_INTEGER, 0, 0,
                                        (SQLPOINTER) dt_integer_u, STRINGMAX ,
                                        ptr_integer_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
            
			if (actions == UPDATE) {
				offset = -1;
			}
			else {
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 19, SQL_PARAM_INPUT, SQL_C_CHAR,
											SQL_BIGINT, 0, 0,
											(SQLPOINTER) dt_largeint, STRINGMAX ,
											ptr_largeint );
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( "SQLBindParameter()", __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}
			}
                     
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 20, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_REAL, 0, 0,
                                        (SQLPOINTER) dt_real, STRINGMAX ,
                                        ptr_real );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 21, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_FLOAT, 0, 0,
                                        (SQLPOINTER) dt_float, STRINGMAX ,
                                        ptr_float );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                        
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 22, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_DOUBLE, 0, 0,
                                        (SQLPOINTER) dt_double_precision, STRINGMAX ,
                                        ptr_double_precision );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                                                                                     
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 23, SQL_PARAM_INPUT, SQL_C_TYPE_DATE ,
                                        SQL_TYPE_DATE, 5, 0, 
                                        (SQLPOINTER) dt_date, 0,
                                        ptr_date );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 24, SQL_PARAM_INPUT, SQL_C_TYPE_TIME ,
                                        SQL_TYPE_TIME, 5, 0, 
                                        (SQLPOINTER) dt_time, 0,
                                        ptr_time );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 25, SQL_PARAM_INPUT, SQL_C_TYPE_TIMESTAMP ,
                                        SQL_TYPE_TIMESTAMP, 5, 0, 
                                        (SQLPOINTER) dt_timestamp, 0,
                                        ptr_timestamp );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 26, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_YEAR, 5, 0, 
                                        (SQLPOINTER) dt_interval_year,0,
                                        ptr_interval_year );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 27, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_MONTH, 5, 0, 
                                        (SQLPOINTER) dt_interval_month, 0,
                                        ptr_interval_month );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 28, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_DAY, 5, 0, 
                                        (SQLPOINTER) dt_interval_day, 0,
                                        ptr_interval_day );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 29, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_HOUR, 5, 0, 
                                        (SQLPOINTER) dt_interval_hour, 0,
                                        ptr_interval_hour );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 30, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_MINUTE, 5, 0, 
                                        (SQLPOINTER) dt_interval_minute, 0,
                                        ptr_interval_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 31, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_SECOND, 5, 0, 
                                        (SQLPOINTER) dt_interval_second, 0,
                                        ptr_interval_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 32, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_YEAR_TO_MONTH, 5, 0, 
                                        (SQLPOINTER) dt_interval_year_to_month, 0,
                                        ptr_interval_year_to_month );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 33, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_DAY_TO_HOUR, 5, 0, 
                                        (SQLPOINTER) dt_interval_day_to_hour, 0,
                                        ptr_interval_day_to_hour );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 34, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_DAY_TO_MINUTE, 5, 0, 
                                        (SQLPOINTER) dt_interval_day_to_minute, 0,
                                        ptr_interval_day_to_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 35, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_DAY_TO_SECOND, 5, 0, 
                                        (SQLPOINTER) dt_interval_day_to_second, 0,
                                        ptr_interval_day_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 36, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_HOUR_TO_MINUTE, 5, 0, 
                                        (SQLPOINTER) dt_interval_hour_to_minute, 0,
                                        ptr_interval_hour_to_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 37, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_HOUR_TO_SECOND, 5, 0, 
                                        (SQLPOINTER) dt_interval_hour_to_second, 0,
                                        ptr_interval_hour_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 38, SQL_PARAM_INPUT, SQL_C_DEFAULT ,
                                        SQL_INTERVAL_MINUTE_TO_SECOND, 5, 0, 
                                        (SQLPOINTER) dt_interval_minute_to_second, 0,
                                        ptr_interval_minute_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }

            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 39, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_NUMERIC, 19, 0,
                                        (SQLPOINTER) dt_bignum_s, STRINGMAX ,
                                        ptr_bignum_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], offset + 40, SQL_PARAM_INPUT, SQL_C_CHAR,
                                        SQL_NUMERIC, 19, 0,
                                        (SQLPOINTER) dt_bignum_u, STRINGMAX ,
                                        ptr_bignum_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindParameter()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }

			if (actions == UPDATE) {
				retcode = SQLBindParameter( handle[ SQL_HANDLE_STMT ], 40, SQL_PARAM_INPUT, SQL_C_CHAR,
											SQL_BIGINT, 0, 0,
											(SQLPOINTER) dt_largeint, STRINGMAX ,
											ptr_largeint );
				if( retcode != SQL_SUCCESS )
				{
					CheckMsgs( "SQLBindParameter()", __LINE__ );
					FreeRowsets( bindOrientations );
					return false;
				}
			}

			break;
    }

	return true;
}

bool BindColsA( int bindOrientations, int testCount ) {
	SQLRETURN  retcode;

	switch( bindOrientations )
    {
        case SINGLE:
        case ROW:
            // Here is where we now bind the C variables to the table columns.
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 1,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_char_iso, STRINGMAX,
                                  &rowset[ 0 ].ptr_char_iso );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 2,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_char_ucs, STRINGMAXDBL,
                                  &rowset[ 0 ].ptr_char_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 3,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_varchar_iso, STRINGMAX,
                                  &rowset[ 0 ].ptr_varchar_iso );                                  
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 4,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_varchar_ucs, STRINGMAXDBL,
                                  &rowset[ 0 ].ptr_varchar_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 5,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_longvarchar_iso, STRINGMAX,
                                  &rowset[ 0 ].ptr_longvarchar_iso );                                  
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 6,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_longvarchar_ucs, STRINGMAXDBL,
                                  &rowset[ 0 ].ptr_longvarchar_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 7,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_nchar, STRINGMAXDBL,
                                  &rowset[ 0 ].ptr_nchar );                                  
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 8,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_ncharvarying, STRINGMAXDBL,
                                  &rowset[ 0 ].ptr_ncharvarying );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 9,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_decimal_s, STRINGMAX,
                                  &rowset[ 0 ].ptr_decimal_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 10,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_decimal_u, STRINGMAX,
                                  &rowset[ 0 ].ptr_decimal_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 11,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_numeric_s, STRINGMAX,
                                  &rowset[ 0 ].ptr_numeric_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 12,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_numeric_u, STRINGMAX,
                                  &rowset[ 0 ].ptr_numeric_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                               
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 13,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_tinyint_s, STRINGMAX,
                                  &rowset[ 0 ].ptr_tinyint_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 14,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_tinyint_u, STRINGMAX,
                                  &rowset[ 0 ].ptr_tinyint_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                  
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 15,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_smallinteger_s, STRINGMAX,
                                  &rowset[ 0 ].ptr_smallinteger_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 16,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_smallinteger_u, STRINGMAX,
                                  &rowset[ 0 ].ptr_smallinteger_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                                       
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 17,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_integer_s, STRINGMAX,
                                  &rowset[ 0 ].ptr_integer_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                  
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 18,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_integer_u, STRINGMAX,
                                  &rowset[ 0 ].ptr_integer_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                  
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 19,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_largeint, STRINGMAX,
                                  &rowset[ 0 ].ptr_largeint );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                     
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 20,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_real, STRINGMAX,
                                  &rowset[ 0 ].ptr_real );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 21,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_float, STRINGMAX,
                                  &rowset[ 0 ].ptr_float );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                  
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 22,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_double_precision, STRINGMAX,
                                  &rowset[ 0 ].ptr_double_precision );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                  
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 23,  SQL_C_TYPE_DATE ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_date, 0,
                                  &rowset[ 0 ].ptr_date );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 24,  SQL_C_TYPE_TIME ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_time, 0,
                                  &rowset[ 0 ].ptr_time );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 25,  SQL_C_TYPE_TIMESTAMP ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_timestamp, 0,
                                  &rowset[ 0 ].ptr_timestamp );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 26,  SQL_C_INTERVAL_YEAR ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_year,0,
                                  &rowset[ 0 ].ptr_interval_year );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 27,  SQL_C_INTERVAL_MONTH ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_month, 0,
                                  &rowset[ 0 ].ptr_interval_month );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 28,  SQL_C_INTERVAL_DAY ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_day, 0,
                                  &rowset[ 0 ].ptr_interval_day );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 29,  SQL_C_INTERVAL_HOUR ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_hour, 0,
                                  &rowset[ 0 ].ptr_interval_hour );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 30,  SQL_C_INTERVAL_MINUTE ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_minute, 0,
                                  &rowset[ 0 ].ptr_interval_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 31,  SQL_C_INTERVAL_SECOND ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_second, 0,
                                  &rowset[ 0 ].ptr_interval_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 32,  SQL_C_INTERVAL_YEAR_TO_MONTH ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_year_to_month, 0,
                                  &rowset[ 0 ].ptr_interval_year_to_month );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 33,  SQL_C_INTERVAL_DAY_TO_HOUR ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_day_to_hour, 0,
                                  &rowset[ 0 ].ptr_interval_day_to_hour );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 34,  SQL_C_INTERVAL_DAY_TO_MINUTE ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_day_to_minute, 0,
                                  &rowset[ 0 ].ptr_interval_day_to_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 35,  SQL_C_INTERVAL_DAY_TO_SECOND ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_day_to_second, 0,
                                  &rowset[ 0 ].ptr_interval_day_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 36,  SQL_C_INTERVAL_HOUR_TO_MINUTE ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_hour_to_minute, 0,
                                  &rowset[ 0 ].ptr_interval_hour_to_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 37,  SQL_C_INTERVAL_HOUR_TO_SECOND ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_hour_to_second, 0,
                                  &rowset[ 0 ].ptr_interval_hour_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 38,  SQL_C_INTERVAL_MINUTE_TO_SECOND ,
                                  (SQLPOINTER) &rowset[ 0 ].dt_interval_minute_to_second, 0,
                                  &rowset[ 0 ].ptr_interval_minute_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }

            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 39,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_bignum_s, STRINGMAX,
                                  &rowset[ 0 ].ptr_bignum_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 40,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_bignum_u, STRINGMAX,
                                  &rowset[ 0 ].ptr_bignum_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }

			break;
        case COLUMN:
            // Here is where we now bind the C variables to the table columns.
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 1,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_char_iso, STRINGMAX,
                                  ptr_char_iso );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 2,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_char_ucs, STRINGMAXDBL,
                                  ptr_char_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 3,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_varchar_iso, STRINGMAX,
                                  ptr_varchar_iso );                                  
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 4,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_varchar_ucs, STRINGMAXDBL,
                                  ptr_varchar_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 5,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_longvarchar_iso, STRINGMAX,
                                  ptr_longvarchar_iso );                                  
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 6,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_longvarchar_ucs, STRINGMAXDBL,
                                  ptr_longvarchar_ucs );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 7,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_nchar, STRINGMAXDBL,
                                  ptr_nchar );                                  
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 8,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_ncharvarying, STRINGMAXDBL,
                                  ptr_ncharvarying );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 9,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_decimal_s, STRINGMAX,
                                  ptr_decimal_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 10,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_decimal_u, STRINGMAX,
                                  ptr_decimal_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 11,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_numeric_s, STRINGMAX,
                                  ptr_numeric_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 12,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_numeric_u, STRINGMAX,
                                  ptr_numeric_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                               
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 13,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_tinyint_s, STRINGMAX,
                                  ptr_tinyint_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 14,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_tinyint_u, STRINGMAX,
                                  ptr_tinyint_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                  
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 15,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_smallinteger_s, STRINGMAX,
                                  ptr_smallinteger_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 16,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_smallinteger_u, STRINGMAX,
                                  ptr_smallinteger_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                                       
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 17,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_integer_s, STRINGMAX,
                                  ptr_integer_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                  
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 18,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_integer_u, STRINGMAX,
                                  ptr_integer_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                  
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 19,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_largeint, STRINGMAX,
                                  ptr_largeint );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                     
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 20,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_real, STRINGMAX,
                                  ptr_real );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 21,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_float, STRINGMAX,
                                  ptr_float );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                  
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 22,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_double_precision, STRINGMAX,
                                  ptr_double_precision );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                                                                                         
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 23,  SQL_C_TYPE_DATE ,
                                  (SQLPOINTER) dt_date, 0,
                                  ptr_date );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 24,  SQL_C_TYPE_TIME ,
                                  (SQLPOINTER) dt_time, 0,
                                  ptr_time );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 25,  SQL_C_TYPE_TIMESTAMP ,
                                  (SQLPOINTER) dt_timestamp, 0,
                                  ptr_timestamp );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 26,  SQL_C_INTERVAL_YEAR ,
                                  (SQLPOINTER) dt_interval_year,0,
                                  ptr_interval_year );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 27,  SQL_C_INTERVAL_MONTH ,
                                  (SQLPOINTER) dt_interval_month, 0,
                                  ptr_interval_month );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 28,  SQL_C_INTERVAL_DAY ,
                                  (SQLPOINTER) dt_interval_day, 0,
                                  ptr_interval_day );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 29,  SQL_C_INTERVAL_HOUR ,
                                  (SQLPOINTER) dt_interval_hour, 0,
                                  ptr_interval_hour );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 30,  SQL_C_INTERVAL_MINUTE ,
                                  (SQLPOINTER) dt_interval_minute, 0,
                                  ptr_interval_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 31,  SQL_C_INTERVAL_SECOND ,
                                  (SQLPOINTER) dt_interval_second, 0,
                                  ptr_interval_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 32,  SQL_C_INTERVAL_YEAR_TO_MONTH ,
                                  (SQLPOINTER) dt_interval_year_to_month, 0,
                                  ptr_interval_year_to_month );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 33,  SQL_C_INTERVAL_DAY_TO_HOUR ,
                                  (SQLPOINTER) dt_interval_day_to_hour, 0,
                                  ptr_interval_day_to_hour );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 34,  SQL_C_INTERVAL_DAY_TO_MINUTE ,
                                  (SQLPOINTER) dt_interval_day_to_minute, 0,
                                  ptr_interval_day_to_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 35,  SQL_C_INTERVAL_DAY_TO_SECOND ,
                                  (SQLPOINTER) dt_interval_day_to_second, 0,
                                  ptr_interval_day_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 36,  SQL_C_INTERVAL_HOUR_TO_MINUTE ,
                                  (SQLPOINTER) dt_interval_hour_to_minute, 0,
                                  ptr_interval_hour_to_minute );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 37,  SQL_C_INTERVAL_HOUR_TO_SECOND ,
                                  (SQLPOINTER) dt_interval_hour_to_second, 0,
                                  ptr_interval_hour_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 38,  SQL_C_INTERVAL_MINUTE_TO_SECOND ,
                                  (SQLPOINTER) dt_interval_minute_to_second, 0,
                                  ptr_interval_minute_to_second );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }

	        retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 39,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_bignum_s, STRINGMAX,
                                  ptr_bignum_s );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
                FreeRowsets( bindOrientations );
                return false;
            }
                
            retcode = SQLBindCol( handle[ SQL_HANDLE_STMT ], 40,  SQL_C_CHAR,
                                  (SQLPOINTER) dt_bignum_u, STRINGMAX,
                                  ptr_bignum_u );
            if( retcode != SQL_SUCCESS )
            {
                CheckMsgs( "SQLBindCol()", __LINE__ );
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
				int injectionTypes,
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
				if ( (tableTypes == MULTISET) || 
					 (injectionTypes == ERR_PER_ROW && rs == 2) ||
					 (injectionTypes == FULL_ERRORS && rs == 2) )
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
				sprintf( (char*)rowset[ rs ].dt_varchar_iso, "%s", "ABCDEFGHIJKLMNOPQRSTUVWXY" );
				break;
			case COLUMN:
				sprintf( (char*)&dt_varchar_iso[ rs * STRINGMAX  ], "%s", "ABCDEFGHIJKLMNOPQRSTUVWXY" );
				break;
		}
		switch ( actions ) {
			case INSERT:
			case UPDATE:
				//assignStatus( rs, SQL_PARAM_SUCCESS_WITH_INFO );
				assignStatus( rs, SQL_PARAM_ERROR );				// Fixed in R2.5
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
	if ((bitflag & B_CHECKCONST) == B_CHECKCONST)
	{
		switch( bindTypes )
		{
			case ROW:
			case SINGLE:
           		sprintf( (char*)rowset[ rs ].dt_integer_s, "%d", 50001 );
				break;
			case COLUMN:
           		sprintf( (char*)&dt_integer_s[ rs * STRINGMAX  ], "%d", 50001 );
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
	            sprintf( (char*)rowset[ rs ].dt_decimal_s, "%d", 123456789 );
				break;
			case COLUMN:
	            sprintf( (char*)&dt_decimal_s[ rs * STRINGMAX  ], "%d", 123456789 );
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
	            sprintf( (char*)rowset[ rs ].dt_decimal_u, "%d", -1);
				break;
			case COLUMN:
	            sprintf( (char*)&dt_decimal_u[ rs * STRINGMAX  ], "%d", -1 );
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

void DisplayTable(int bindOrientations, int numRows) {
	int i = 0;
	while(i < numRows)
		DisplayRowsets(bindOrientations, i++);
}

int GeneratingRows( int rowsetSizes, int numberOfRows, int injectionTypes, int tableTypes, int actions, int bindOrientations ) {

    int  numberOfRowsHandled = 0;
	int  rs;
    int  cidx = 0;

	numberOfRowsHandled = 0;
    failureInjectionCount = 0;
	goodRowCount = 0;
        printf("rowsetsizes= %d, numberofRows=%d, injectionTypes=%d,tabletypes=%d, actions=%d, bindorientations=%d\n",rowsetSizes,numberOfRows,injectionTypes,tableTypes,actions,bindOrientations);
    // Assign the values in the rowsetnumberOfRows
    for( rs = 0; ( rs < rowsetSizes ) && ( rs < numberOfRows )&& ( numberOfRowsHandled < numberOfRows ); rs++ )
    {
		unsigned int bitflag = 0;
        switch( injectionTypes )
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
                    if( tableTypes == MULTISET )
                    {
						goodRowCount++;
						if ( actions == UPDATE )
							goodRowCount += 3;
                    }
					else
					{
						if ( actions == UPDATE )
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
					if( tableTypes == MULTISET )
					{
						goodRowCount++;
						if ( actions == UPDATE )
							goodRowCount += 3;
					}
					else
					{
						if ( actions == UPDATE )
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
					//goodRowCount++;
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
						if ( tableTypes != VOLATILE )
							bitflag = B_CHECKCONST;
						else
							bitflag = B_TIMESTAMP;;
						break;
					case 1:			//String overflow
						bitflag = B_STRINGOVERFLOW;
						//goodRowCount++;
						break;
					case 2:			//Duplicated key  - This row got inserted
						bitflag = B_DUPLICATEKEY;
						//The Multiset tables is excepting duplicate keys
						if( tableTypes == MULTISET )
						{
							goodRowCount++;
							//if ( actions == UPDATE )
							//	goodRowCount += 5;			//B_SRINGOVERFLOW returns in error previously in INSERT
						}
						else
						{
							if ( actions == UPDATE || actions == DELETE_PARAM || actions == INSERT || actions == SELECT)
								goodRowCount++;
						}
						break;
					case 3:			//Duplicated rows
						bitflag = B_DUPLICATEROW | B_STRINGOVERFLOW;
						//The Multiset tables is excepting duplicate rows
						//But because STRINGOVERFLOW, the row is rejected as ERROR
						//if( tableTypes == MULTISET )
						//{
						//	goodRowCount++;
						//	if ( actions == UPDATE )
						//		goodRowCount += 5;
						//}
						//else
						//{
						//	if ( actions == UPDATE )
						//		goodRowCount++;
						//}
						break;
					case 4:			//Null value
						bitflag = B_NULLVALUE;
						break;
					case 5:			//Date, Time or Timestamp can not be converted
						bitflag = B_STRINGOVERFLOW;
						//goodRowCount++;
						break;
					case 6:			//Divided by zero
						bitflag = B_STRINGOVERFLOW;
						//goodRowCount++;
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
			case FULL_ERRORS: // Some rows got inserted and updated, especially in MODE1
				switch ( rs % 10) {
					case 0:	case 1: case 4: case 6: case 8: //String overflow
						bitflag = B_STRINGOVERFLOW;
						//goodRowCount++;
						break;
					case 2:	//Duplicated Key  - only this row got inserted
						bitflag = B_DUPLICATEKEY;
						//The Multiset tables is excepting duplicate keys
						if( tableTypes == MULTISET )
						{
							goodRowCount++;
							if ( actions == UPDATE )
								goodRowCount += 10;       
						}
						else
						{
							if ( actions == UPDATE || actions == SELECT || actions == DELETE_PARAM || actions == INSERT )
								goodRowCount++;
						}
						break;
					case 3: case 5: case 7: case 9:	//Duplicated Key
						bitflag = B_DUPLICATEKEY;
						//The Multiset tables is excepting duplicate keys
						if( tableTypes == MULTISET )
						{
							goodRowCount++;
							if ( actions == UPDATE && (rs%10)==3 )
								goodRowCount += 10;        
						}
						else
						{
							if ( actions == UPDATE )
								goodRowCount++;
						}
						break;
				}
				break;
			/***********************************************************************/
			/***********************************************************************/
			case DRIVER_GOOD_BAD_MULCOL://Some good rows, some error, no warning, multiple columns
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
						//goodRowCount++;
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
						//goodRowCount++;
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
				switch ( rs % 10) {		// B_STRINGOVERFLOW is considered as error in R2.5
					case 0: case 2: case 4: case 6: case 8:	case 9: //String overflow (this is the only warning I know so far)
						bitflag = B_STRINGOVERFLOW;
						//goodRowCount++;
						break;
					case 1:	case 3:	case 5:	case 7:			
						bitflag = B_STRINGOVERFLOW;
						//goodRowCount++;
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
						//goodRowCount++;
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
                        // B_STRINGOVERFLOW returns ERROR in R2.5
						//if( tableTypes == MULTISET )
						//{
						//	goodRowCount++;             
						//	if ( actions == UPDATE )
						//	    goodRowCount += 4;
						//}
						//else
						//{
						//	if ( actions == UPDATE );
						//		goodRowCount++;		
						//}
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
						//if (tableTypes != VOLATILE)
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
						if (tableTypes != VOLATILE) {
							bitflag = B_DUPLICATEKEY | B_CHECKCONST;
						}
						else
							bitflag = B_DUPLICATEKEY | B_NUMERICOVERFLOW;
						break;
					case 2:	case 5:	case 7: //String overflow
						bitflag = B_STRINGOVERFLOW;
						//goodRowCount++;
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
						if (tableTypes != VOLATILE) {
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
						//goodRowCount++;
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
						//if (tableTypes != VOLATILE) {
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
						//goodRowCount++;
						break;
					case 2: case 5: case 8:	//Server error: Duplicated Key, String overflow
						bitflag = B_DUPLICATEKEY | B_STRINGOVERFLOW;
						//The Multiset tables is excepting duplicate keys
                        // B_STRINGOVERFLOW returns error in R2.5
						//if( tableTypes == MULTISET )
						//{
						//	goodRowCount++;
						//	if ( actions == UPDATE )
						//		goodRowCount += 7;
						//}
						//else
						//{
						//	if ( actions == UPDATE );
						//		goodRowCount++;
						//}
						break;
				}
				break;
			/***********************************************************************/
			/***********************************************************************/
			default:
                RecordToLog( " >> INTERNAL ERROR: An unknown failure type has been discovered.\n" );
                break;
        }

		DML_A_ROW(  bitflag, actions, tableTypes, bindOrientations, injectionTypes, rs, &failureInjectionCount, numberOfRowsHandled );

		if (debug) DisplayRowsets(bindOrientations, rs);

        numberOfRowsHandled++;
    } // end of FOR-LOOP

	return rs;
}


#endif /* ROWSETS_H */
