#ifndef __GLOBALSH      /* this prevents multiple copies of this... */
#define __GLOBALSH      /* ...include file from being #included... */

//******************************************************************
//** GLOBALS.H - External declarations for global variables
//*******************************************************************
#include "defines.h"
#include "commonglobals.h"

// input parameter values
extern long gVersion;					// version number of input file format
extern int gProcessNumber;          // This process's Process number
extern int gPid;                    // this process's pid
extern long gMasterSeed;				// Master random number gen. seed printed
													// in each logfile so the test can be
													// repeated
extern long gSeed;						// number used to prime random number gen.
extern long gCheckInterval;			// time interval for checking consistency
extern long gRuntime;					// run time (in minutes)
extern time_t g_start_time;			// global starting time
extern list_desc *gpList[MAX_LOOPS];
extern long gTableCount;				// number of tables to use
extern table_description *gpTableDesc[MAX_TABLES];
extern long min_subset_size;			// smallest subset size
extern long max_subset_size;			// largest subset size
extern long min_vsbb_size;		   	// smallest VSBB size
extern long max_vsbb_size;		   	// largest VSBB size
extern long abort_trans;				// abort percentage
extern long dtc_trans;					// dtc percentage
extern long max_actions_per_trans;	// max. number of actions per transaction
extern long min_actions_per_trans;	// min. number of actions per transaction
extern long max_concurrent_trans;	// max. number of concurrent transactions
extern long min_concurrent_trans;	// min. number of concurrent transactions
extern long g_percent[MAX_ACTION_TYPES];				// percents for each action to be executed

extern long gTmp_fnum;					// filenumber for TMF's TMP
extern char gSqlCatalog[MAX_TABLE_NAME_LEN];				// name of SQL catalog
extern char gStartFile[MAX_TABLE_NAME_LEN];				// name of master's startup file
extern char gStopFile[MAX_TABLE_NAME_LEN];				// name of master's stop file
extern char g_status_file[MAX_TABLE_NAME_LEN];			// name of this process's status file
extern char g_testid_dir[MAX_TABLE_NAME_LEN];		// dir for this testid
extern char g_errstr[20];				// error string prefix
extern char g_errindent[20];			// indent for error prefix
extern long g_action_count;			// counter used in status file postings
extern long g_trans_commit;			// counter used in status file postings
extern long g_trans_abort;				// counter used in status file postings
extern long  gAddColPositive;	   	// counter used in add column positive test
extern long  gAddColNegative;	   	// counter used in add column negative test
//extern long  gDataType[];			// array of data types for add column
//extern long  gDataTypeCount;		// number of data types for add column


#endif
