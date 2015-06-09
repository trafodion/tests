#ifndef __STRUCTH      /* this prevents multiple copies of this... */
#define __STRUCTH      /* ...include file from being #included... */

#include "bitlib.h"
/*************************************************************************
** STRUCT.H
** Contains structure definitions used throughout
*************************************************************************/
struct key_info{
	short ColNum;
	char *DefaultValue;
	};
typedef struct key_info key_info;

struct table_description {
   char TableName[SQL_MAX_DSN_LENGTH];
   TableInfo *pTable;
   short Organization;
   short process_count;
   long max_records;
   short key_column_used;
   short zerosum_column;
   short abort_column;
   short last_process_id_column;
   short key_column_count;
   key_info *key_ptr;
   Boolean full;
   long min_range;
   long max_range;
   Bitmap *BitmapPtr;
   HENV henv;
   HDBC hdbc;
   HSTMT hstmt;
   };
typedef struct table_description table_description;

struct list_desc {
   short item_count;
   short duration;
   struct item_desc {
      short code;
      union {
         short number;
         short loop_number;
         short percentage;
         short repetitions;
         } u1;
      } item[1];
   };
typedef struct list_desc list_desc;

#endif
