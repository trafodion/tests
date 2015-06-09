//******************************************************************
//** GLOBALS.C - Declarations for global variables
//*******************************************************************
#include "commonglobals.c"
// input parameter values
long gVersion;						// version number of input file format
long gProcessNumber;				// This process's Process number
int gPid;                     // this process's pid
long gMasterSeed;					// Master random number gen. seed printed
											// in each logfile so the test can be
											// repeated
long gSeed;							// number used to prime random number gen.
long gCheckInterval;				// time interval for checking consistency
long gRuntime;						// run time (in minutes)
time_t g_start_time;				// global starting time
list_desc *gpList[MAX_LOOPS];	//list of actions
long gTableCount;					// number of tables to use
table_description *gpTableDesc[MAX_TABLES];
long min_subset_size;			// smallest subset size
long max_subset_size;			// largest subset size
long min_vsbb_size;				// smallest VSBB size
long max_vsbb_size;				// largest VSBB size
long abort_trans;					// abort percentage
long dtc_trans;					// DTC percentage
long max_actions_per_trans;	// max. number of actions per transaction
long min_actions_per_trans;	// min. number of actions per transaction
long max_concurrent_trans;		// max. number of concurrent transactions
long min_concurrent_trans;		// min. number of concurrent transactions
long g_percent[MAX_ACTION_TYPES];	// percents for each action to be executed

long gTmp_fnum;					// filenumber for TMF's TMP
char gSqlCatalog[MAX_TABLE_NAME_LEN];		// name of SQL catalog
char gStartFile[MAX_TABLE_NAME_LEN];		// name of master's startup file
char gStopFile[MAX_TABLE_NAME_LEN];			// name of master's stop file
char g_status_file[MAX_TABLE_NAME_LEN];	// name of this process's status file
char g_testid_dir[MAX_TABLE_NAME_LEN];	// directory for this testid
char g_errstr[20];				// error string prefix
char g_errindent[20];			// indent for error prefix
long g_action_count;				// counter used in status file postings
long g_trans_commit;				// counter used in status file postings
long g_trans_abort;				// counter used in status file postings
long  gAddColPositive;			// counter used in add column positive test
long  gAddColNegative;			// counter used in add column negative test
//long  gDataType[];				// array of data types for add column
//long  gDataTypeCount;			// number of data types for add column
