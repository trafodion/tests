#ifndef __TOKENSH      /* this prevents multiple copies of this... */
#define __TOKENSH      /* ...include file from being #included... */

/* token values */
#define INVALID_CHARACTER    0
#define COMMA                1
#define SEMI_COLON           2
#define DASH                 3
#define EQUALS               4
#define BEGIN_LIST           5
#define END_LIST             6
#define BEGIN_BLOCK          7
#define END_BLOCK            8

#define STRING               9
#define NUMBER              10
#define PROCESS_N           11
#define TABLE_N             12

#define STARTUP             13
#define ALL_PROCESSES       14
#define CLEANUP             15
#define CREATE_KW           16
#define USE                 17
#define MAX_RECORDS         18
#define RECORD_RANGE        19
#define REPEAT              20
#define PROCESS             21
#define KEY_SEQ_KW          22
#define ENTRY_SEQ_KW        23
#define RELATIVE_KW         24
#define TABLE               25
#define LIKE                26
#define WITH                27
#define COLUMNS             28
#define ABORT_KW            29
#define FOR_KW              30
#define MINUTES             31
#define HOURS               32
#define FOREVER             33
#define RANDOM_KW           34
#define SEQUENTIAL          35
#define TESTID              36
#define WORK_VOL            37
#define TABLE_VOL           38
#define INSERT              39
#define DELETE_ROW          40
#define UPDATE              41
#define SELECT              42
#define TIMES               43
#define ALL                 44
#define TRANSACTION_SIZE    45
#define CONCURRENT_CONNECTIONS     46
#define SUBSET_SIZE         47
#define VSBB_SIZE           48
#define RUNTIME             49
#define SEED                50
#define CHECK_INTERVAL      51
#define UNTIL_DONE          52
#define VSBB                53
#define LIBRARY             54
#define FILL                55
#define RECORD              56
#define TO_KW               57
#define AUDITED             58
#define NONAUDITED          59
#define ADD                 60
#define COLUMN              61
#define ALTER_KW            62
#define UPDATE_M            63
#define SETTESTPOINT        64
#define CLEARTESTPOINT      65
#define DTC_TRANSACTIONS    66
#define STOP_ON_ERROR_KW    67

#endif
