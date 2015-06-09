#ifndef __BITLIBH      /* this prevents multiple copies of this... */
#define __BITLIBH      /* ...include file from being #included... */

/***********************************************************************
** BITLIB.H
** This include file contains the external declarations and any needed
** typedefs and defines for the functions in BITLIB.C.
***********************************************************************/

/************
** defines **
************/

/* Valid values for <flag> */
#define BIT_ON       1
#define BIT_OFF      0

/* Valid values for <search_type> */
#define SEARCH_UNTIL_END    0
#define CIRCULAR_SEARCH     1

/* Valid return values */
#define BIT_NOT_FOUND      -1


/**************************
** external declarations **
**************************/


/****************************/
/** Older bitmap functions **/
/****************************/

typedef char bitmap;

extern long find_next_bit(int flag,bitmap *bitmap_ptr,long table_len,
                         long start_offset,int search_type);
extern void set_bit(int flag,bitmap *bitmap_ptr,long offset);
extern void set_bitblock(int flag,bitmap *bitmap_ptr,long offset,
                         long max_size,long block_size);
extern long find_next_bitblock(int flag,bitmap *bitmap_ptr,long table_len,
                               long start_offset,int search_type,
                               long block_size,long *actual_block_size);
extern long count_bits(int flag,bitmap *bitmap_ptr,long bitmap_len);


/****************************/
/** Newer Bitmap functions **/
/****************************/

struct Bitmap {
   long MapLen;
   char *MapPtr;
   };
typedef struct Bitmap Bitmap;

extern Bitmap *QACreateBitmap(long BitmapSize);
extern void FreeBitmap(Bitmap *BitmapPtr);
extern void SetBitBlock(int Flag,Bitmap *BitmapPtr,long StartingOffset,
                        long BlockSize);
extern void SetBit(int Flag,Bitmap *BitmapPtr,long Offset);
extern long FindNextBit(int Flag,Bitmap *BitmapPtr,
                        long StartOffset,int SearchType);
extern long FindNextBitBlock(int Flag,Bitmap *BitmapPtr,
                             long StartOffset,int SearchType,
                             long RequestedBlockSize,long *ActualBlockSize);
extern long CountBits(int Flag,Bitmap *BitmapPtr);
extern void CopyBitmap(Bitmap *pToBitmap,Bitmap *pFromBitmap);

#endif
