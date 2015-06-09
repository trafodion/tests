#ifndef __MSTRUCTH      /* this prevents multiple copies of this... */
#define __MSTRUCTH      /* ...include file from being #included... */

/************************************************************************
** MSTRUCT.H
** Contains structure definitions used throughout NomadPC Master
*************************************************************************/

#include "bitlib.h"

/* in Posix, the following are defined in stat.h */
/* so I just stole them from cygwin and put them here */
//#define	S_IRWXU 	(S_IRUSR | S_IWUSR | S_IXUSR)
//#define		S_IRUSR	0000400	/* read permission, owner */
//#define		S_IWUSR	0000200	/* write permission, owner */
//#define		S_IXUSR 0000100/* execute/search permission, owner */
//#define	S_IRWXG		(S_IRGRP | S_IWGRP | S_IXGRP)
//#define		S_IRGRP	0000040	/* read permission, group */
//#define		S_IWGRP	0000020	/* write permission, grougroup */
//#define		S_IXGRP 0000010/* execute/search permission, group */
//#define	S_IRWXO		(S_IROTH | S_IWOTH | S_IXOTH)
//#define		S_IROTH	0000004	/* read permission, other */
//#define		S_IWOTH	0000002	/* write permission, other */
//#define		S_IXOTH 0000001/* execute/search permission, other */
/* end of posix steal */

struct key_info{
	short ColNum;
	char *DefaultValue;
	};
typedef struct key_info key_info;

struct NomadInfo {
   char like_name[SQL_MAX_TABLE_NAME_LEN];
   short process_count;
   long max_records;
   long InitialRecordCount;
   short InitialFillMethod;
   short key_column_count;
   key_info *key_ptr;
   short key_column_used;
   short zerosum_column;
   short abort_column;
   short last_process_id_column;
   Bitmap *BitmapPtr;
   };
typedef struct NomadInfo NomadInfo;

/* information related to a specific SQL table */
struct TableDescription {
   NomadInfo *NomadInfoPtr;
   TableInfo *TableInfoPtr;
	HENV	henv;
	HDBC	hdbc;
	HSTMT	hstmt;
   };
typedef struct TableDescription TableDescription;

/* information for a specific process about the table(s) it is using */
struct table {
   short num;
   long min_range;
   long max_range;
   struct table *next_ptr;
   };
typedef struct table table;

struct list_desc;  /* forward declaration of <list_desc> */

struct item_desc {
   short code;
   short number;  /* list number, percentage, or repetition count */
   struct list_desc *list_ptr; /* used only if <code>==REPEAT_LOOP */
   struct item_desc *next_ptr;
   };
typedef struct item_desc item_desc;

struct list_desc {
   short item_count;
   short duration;
   item_desc *first_item_ptr;
   item_desc *last_item_ptr;
   };
typedef struct list_desc list_desc;

struct process_info {
   short like_process;
   short seed;
   short consist_check;
   short table_count;
   table *table_ptr;
   short min_subset_size;
   short max_subset_size;
   short min_vsbb_size;
   short max_vsbb_size;
   short abort_percent;
	short dtc_percent;
   short min_concurrent_trans;
   short max_concurrent_trans;
   short min_trans_size;
   short max_trans_size;
   short trace_options;
   short debug_options;
   short list_count;
	char DataSource[MAX_DATASOURCE_NAME];
	char UID[MAX_UID];
	char PWD[MAX_PWD];
   list_desc list;
   };
typedef struct process_info process_info;

struct testid_info{
   short process_count;
   short tables_created;
   char table_prefix[_MAX_PATH];
   short tables_used;
   char sql_catalog[_MAX_PATH];
	char sql_schema[_MAX_PATH];
   char test_vol[_MAX_PATH];
   char infile[_MAX_PATH];
   };
typedef struct testid_info testid_info;

struct test_desc{
   char testid[3];
   unsigned short RandomSeed;
   char library[_MAX_PATH];
   char work_volume[_MAX_PATH];
   char catalog[_MAX_PATH];
   char object_file[_MAX_PATH];
   short table_count;
   TableDescription *table_ptr[MAX_TABLES];
   short process_count;
   process_info *process_ptr[MAX_PROCESSES];
   };
typedef struct test_desc test_desc;

#endif
