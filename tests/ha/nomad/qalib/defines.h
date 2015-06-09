#ifndef __DEFINESH
#define __DEFINESH

#undef NULL				// redefine NULL to prevent compiler warnings
#define NULL '\0'


#define BLANK	' '
#define TAB		'\t'

/* std_err() error message values */
#define MISSING_EQUALS             1
#define MISSING_SEMI_COLON         2
#define MISSING_COMMA              3
#define MISSING_COLON              4
#define MISSING_OPEN_PAREN         5
#define MISSING_CLOSE_PAREN        6

/* defines for PROCESS_CREATE_ procedure call */
#define PROC_NAME_SUPPLIED         1

/* FILE_GETINFOLISTBYNAME_ item codes */
#define FILE_TYPE                 41
#define FILE_CODE                 42
#define SQL_CATALOG_LENGTH        84
#define SQL_CATALOG               85

/* maximums and minimums used throughout */
#define MAX_PROCESSES             999
#define MAX_VOLUME_LEN            17   /* enough for \xxxxxxx.$xxxxxxx */
#define MAX_LINE                  80
#define NOMAD_MIN_COLUMN_COUNT    4
#define _MAX_PATH                 300

/* action codes */
#define REPEAT_LOOP                0
#define RANDOM_INSERT              1
#define RANDOM_UPDATE              2
#define RANDOM_DELETE              3
#define RANDOM_SELECT              4
#define SEQ_INSERT                 5
#define SEQ_UPDATE                 6
#define SEQ_DELETE                 7
#define SEQ_SELECT                 8
#define VSBB_INSERT                9
#define VSBB_UPDATE               10
#define VSBB_SELECT               11
#define SEQ_INSERT_ALL            12
#define SEQ_UPDATE_ALL            13
#define SEQ_DELETE_ALL            14
#define SEQ_SELECT_ALL            15
#define VSBB_INSERT_ALL           16
#define VSBB_UPDATE_ALL           17
#define VSBB_SELECT_ALL           18
#define RANDOM_INSERT_ALL         19
#define RANDOM_UPDATE_ALL         20
#define RANDOM_DELETE_ALL         21
#define RANDOM_SELECT_ALL         22
//#define ALTER_ADD_COL             23
#define DO_NOTHING             -1000

#define MAX_ACTION_TYPES          23


/* other misc defines */
#define VERSION                    9
#define DISK_DEVICE_TYPE           3
#define NOMAD_CONFIG_FILE          "Nomad.conf"
#define OBJECT_FILECODE            100

#define FILLRANDOMLY               1
#define FILLSEQUENTIALLY           2

#define STARTUP_SECTION           -1
#define ALL_PROCESSES_SECTION     -2
#define CLEANUP_SECTION           -3


/* defines for trace and debug options */
#define TRACE_TOKENS               1
#define TRACE_FUNCTIONS            2
#define TRACE_SQL                  4
#define TRACE_8                    8
#define TRACE_16                  16
#define TRACE_32                  32
#define TRACE_64                  64
#define TRACE_128                128

/* some defines to make coding easier */
#define BuildReturnStatusMALLOC   BuildReturnStatus(RT_MALLOC,0,NULL,NULL)

/*********************************************************************
** DEFINES2.H - contains globally used #defines
*********************************************************************/

#define MAX_TABLES               10
#define MAX_LOOPS               100
#define MAX_CONCURRENT_TRANS     10
#define MAX_TABLE_NAME_LEN       35
#define SQL_MAX_COMMAND_LENGTH	16383	// SQLGetInfo(SQL_MAX_STATEMENT_LEN)
													// should be used to set this but,
													// it doesn't work so I'll hard code
													// it
#define SQL_MAX_KEY_LENGTH			256
#define SQL_MAX_ERROR_MSG			200
#define MAX_DATASOURCE_NAME		50
#define MAX_UID						30
#define MAX_PWD						30

#define DISK_DEVICE_TYPE         3

#define KEY_SEQ                 0
#define ENTRY_SEQ               1
#define RELATIVE_TABLE          2

/* SQL Key type defines */
#define SYSTEM_KEY          0
#define PRIMARY_KEY         1
#define CLUSTERING_KEY      2

/* used by <g_percent> array */
#define NOT_SPECIFIED     -1

#define FS_TIMEOUT        40


/* literals (used for indexing into PERCENT[] array) */
/*
#define INSERT_SINGLE      0
#define UPDATE_SINGLE      1
#define DELETE_SINGLE      2
#define SELECT_SINGLE      3
#define INSERT_RANGE       4
#define UPDATE_RANGE       5
#define DELETE_RANGE       6
#define SELECT_RANGE       7
#define INSERT_VSBB        8
#define UPDATE_VSBB        9
#define SELECT_VSBB       10
#define INSERT_SEQ_ALL    11
#define UPDATE_SEQ_ALL    12
#define DELETE_SEQ_ALL    13
#define SELECT_SEQ_ALL    14
#define INSERT_VSBB_ALL   15
#define UPDATE_VSBB_ALL   16
#define SELECT_VSBB_ALL   17
#define INSERT_RANDOM_ALL 18
#define DELETE_RANDOM_ALL 19
#define UPDATE_RANDOM_ALL 20
#define SELECT_RANDOM_ALL 21
*/
//#define ALTER_ADD_COLUMN  22
//#define CREATE_DROP_TABLE 23
//#define CREATE_KEEP_TABLE 24

#define RETRY_COUNT        5
#define POSITIVE_TEST     100
#define NEGATIVE_TEST    -100

#endif
