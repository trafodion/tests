/***********************************************************************
** bitlib.c
** This source module contains several functions which work with
** bitmaps.
**
** Functions :
**
**    These functions use the 'bitmap' data type and a separate length value
**
**       find_next_bit()
**       find_next_bitblock()
**       set_bit()
**       count_bits()
**       set_bitblock()
**
**    These functions use the 'Bitmap' structure data type which includes the
**    length value.
**
**       QACreateBitmap()
**       FreeBitmap()
**       SetBit()
**       SetBitBlock()
**       FindNextBit()
**       FindNextBitBlock()
**       CountBits()
**       CopyBitmap()
**
**  NOTE: You should use one or the other (preferable the second set)
**        but, not functions from both
***********************************************************************/

#include <stdlib.h>
#include <stdio.h>
#include <memory.h>
#include <assert.h>

//#include "defines.h"
#include "util.h"
#include "bitlib.h"

/**********************************************************************
** Globals (these globals are only known to the functions contained
** within this source module)
***********************************************************************/
char byte_mask[8]={0x80,0x40,0x20,0x10,0x08,0x04,0x02,0x01};


/***********************************************************************
** find_next_bit()
** This function will start searching through a bitmap in one of several
** ways for the next bit set to either ON or OFF depending on what
** was specified by the caller.  The search starts with the starting
** bit position.
**
** Inputs: bit setting to search for
**         pointer to bitmap
**         length of bitmap (in bits)
**         bit position to start searching from
**         type of search (i.e. CIRCULAR_SEARCH, UNTIL_END, etc.)
**   >>> need to implement other types of searches like reverse, etc.
**
** Returns: bit offset of searched for bit if successful
**          -1 if bit not found
***********************************************************************/
long find_next_bit(int flag,bitmap *bitmap_ptr,long max_offset,
                  long start_offset,int search_type)
{
   long bit_offset;
   long byte_offset;
   bitmap *ptr;
   Boolean bit_found;
   long i;
   long offset;
   char temp_char;

   offset=start_offset;
   byte_offset=start_offset/8;
   bit_offset=start_offset%8;
   ptr=bitmap_ptr+byte_offset;

   /* check until end of bitmap is reached */
   bit_found=FALSE;
   while((offset<max_offset)&&(!bit_found)){
      i=bit_offset;
      while((i<8)&&(!bit_found)&&(offset<max_offset)){
         temp_char=*ptr&byte_mask[i];
         if(((flag==BIT_OFF)&&(temp_char==0))||
            ((flag==BIT_ON)&&(temp_char!=0))){
               bit_found=TRUE;
               }
         else{
            offset++;
            i++;
            }
         }
      ptr++;
      bit_offset=0;
      }

   if(bit_found) return(offset);

   if(search_type!=CIRCULAR_SEARCH) return(BIT_NOT_FOUND);

   /* hit end of bitmap, now go back to beginning and search up */
   /* to the starting point, like a circular list */
   offset=0;
   bit_offset=0;
   ptr=bitmap_ptr;

   /* check until at start search position in bitmap is reached */
   bit_found=FALSE;
   while((offset<start_offset)&&(!bit_found)){
      i=bit_offset;
      while((i<8)&&(!bit_found)&&(offset<start_offset)){
         temp_char=*ptr&byte_mask[i];
         if(((flag==BIT_OFF)&&(temp_char==0))||
            ((flag==BIT_ON)&&(temp_char!=0))){
            bit_found=TRUE;
            }
         else{
            offset++;
            i++;
            }
         }
      ptr++;
      bit_offset=0;
      }

   if(bit_found) return(offset);
   return(BIT_NOT_FOUND); /* no bit found */

   }

/***********************************************************************
** find_next_bitblock()
** This function will start searching through a bitmap in one of several
** ways for the next block of bits set to either ON or OFF depending on
** what was specified by the caller.  The search starts with the starting
** bit position.  If the requested block size is not available then the
** next best block size is returned (sort of a largest available).
**
** Inputs: bit setting to search for
**         pointer to bitmap
**         length of bitmap (in bits)
**         bit position to start searching from
**         type of search (i.e. CIRCULAR_SEARCH, UNTIL_END, etc.)
**   >>> need to implement other types of searches
**         requested block size (in bits)
**         actual block size (in bits)
**
** Returns: bit offset of searched for bitblock if successful
**          -1 if no bitblock available
***********************************************************************/
long find_next_bitblock(int flag,bitmap *bitmap_ptr,long max_offset,
                        long start_offset,int search_type,long block_size,
                        long *actual_bitblock_size)
{
   long record_num1;
   long record_num2;
   long first_record_num;
   long temp_size;
   long temp_rec_num;
   int flag1;
   int flag2;
   Boolean first_time_thru_loop;
   Boolean done;
   *actual_bitblock_size=0;

   flag1=flag;
   if(flag1==BIT_ON) flag2=BIT_OFF;
   else flag2=BIT_ON;

   /* find a starting bit of a possible bitblock */
   record_num1=find_next_bit(flag1,bitmap_ptr,max_offset,
                             start_offset,search_type);
   /* if no starting bit found then return the error */
   if(record_num1<0) return(record_num1);

   first_time_thru_loop=TRUE;
   done=FALSE;
   while(!done){

      /* starting bit found, now find ending bit of possible bitblock */
      record_num2=find_next_bit(flag2,bitmap_ptr,max_offset,
                                record_num1,search_type);

      /* handle case where we find the end of a bitblock */
      if(record_num2>record_num1){
          temp_size=record_num2-record_num1;
          }

      else if(record_num2==BIT_NOT_FOUND){
         if(search_type==SEARCH_UNTIL_END){
            temp_size=max_offset-record_num1;

            /* handle case where bitblock just fits at end of bitmap */
            if(temp_size>=block_size) {
               *actual_bitblock_size=block_size;
               return(record_num1);
               }

            /* see if it qualifies to be the biggest block */
            if(temp_size>*actual_bitblock_size){
               *actual_bitblock_size=temp_size;
               return(record_num1);
               }
            return(temp_rec_num);
            }

         /* handle case where all the bits in the bitmap are the same */
         else if (search_type==CIRCULAR_SEARCH){
            *actual_bitblock_size=block_size;
            return(record_num1);
            }
         }

      /* handle case where bitblock wraps from the end to the beginning */
      else if(record_num2<record_num1){
      	temp_size=max_offset-record_num1+record_num2;
         }

      /* if block found is big enough then return */
      if(temp_size>=block_size) {
         *actual_bitblock_size=block_size;
         return(record_num1);
         }

      /* otherwise, see if it qualifies to be the biggest block, so far */
      if(temp_size>*actual_bitblock_size){
         *actual_bitblock_size=temp_size;
         temp_rec_num=record_num1;
         }

      /* find another starting bit of a possible bitblock */
      record_num1=find_next_bit(flag1,bitmap_ptr,max_offset,
                                record_num2,search_type);
      if(first_time_thru_loop){
         first_time_thru_loop=FALSE;
         first_record_num=record_num1;
         }
      else {
         if(first_record_num==record_num1) {
         	done=TRUE;
            }
         }

      } /* end of while(... */

      /* requested blocksize not found so return largest available block */
      return(temp_rec_num);
   }

/***********************************************************************
** set_bit()
** This function will set the bit specified in <bit_position> to either
** ON or OFF depending on which was specified in the function call.
**
** Inputs: bit setting (either ON or OFF, 1 or 0)
**         pointer to bitmap
**         bit position to be set
** Returns: void
************************************************************************/
void set_bit(int flag,bitmap *bitmap_ptr,long bit_position)
{
   long bit_offset;
   long byte_offset;

   byte_offset=bit_position/8;
   bit_offset=bit_position%8;
   bitmap_ptr+=byte_offset;
   if(flag!=BIT_OFF){
      *bitmap_ptr|=byte_mask[bit_offset];    /* turn bit on */
      }
   else{
      *bitmap_ptr^=0xff;                     /* turn bit off */
      *bitmap_ptr|=byte_mask[bit_offset];
      *bitmap_ptr^=0xff;
      }
   }

/***********************************************************************
** count_bits()
**
** This function will count the number of bits (either ON or OFF bits
** can be counted)
**
** Inputs: bit setting to count
**         pointer to bitmap
**         length of bitmap (in bits)
**
** Returns: count of bits
************************************************************************/
long count_bits(int flag,bitmap *bitmap_ptr,long max_offset)
{
   long bit_offset;
   bitmap *ptr;
   long offset;
   long bit_count;
   char temp_char;

   bit_count=0;
   offset=0;
   bit_offset=0;
   ptr=bitmap_ptr;

   /* count until end of bitmap is reached */
   while(offset<max_offset){
      while((bit_offset<8)&&(offset<max_offset)){
         temp_char=*ptr&byte_mask[bit_offset];
         if(((flag==BIT_OFF)&&(temp_char==0))||
            ((flag==BIT_ON)&&(temp_char!=0))){
               bit_count++;
               }
         offset++;
         bit_offset++;
         }
      ptr++;
      bit_offset=0;
      }

   return(bit_count);
   } /* end: count_bits() */

/***********************************************************************
** set_bitblock()
** This function will set the block of bits starting at <bit_position> to
** ON or OFF depending on which was specified in the function call.  If
** the block size goes beyond the end of the bitmap, then it is
** automatically wrapped around to the beginning of the bitmap.
**
** Inputs: bit setting (either ON or OFF, 1 or 0)
**         pointer to bitmap
**         bit position to be set
**         max size of bitmap
**         size of block (in bits)
** Returns: void
************************************************************************/
void set_bitblock(int flag,bitmap *bitmap_ptr,long bit_position,
                  long max_size,long block_size)
{

   long i;
   long last_bit_position;
   last_bit_position=bit_position+block_size-1;
   if(last_bit_position>max_size-1){
      last_bit_position=last_bit_position-max_size;
      for(i=bit_position;i<max_size;i++){
         set_bit(flag,bitmap_ptr,i);
         }
      for(i=0;i<=last_bit_position;i++){
         set_bit(flag,bitmap_ptr,i);
         }
      }
   else {
      for(i=bit_position;i<=last_bit_position;i++){
         set_bit(flag,bitmap_ptr,i);
         }
      }
   }

/***********************************************************************
** QACreateBitmap()
**
** This function allocates and initializes a bitmap structure used by
** all other functions in this module.
**
** Input: size of bitmap (maximum number of bits in bitmap)
**
** Returns: pointer to bitmap structure
************************************************************************/
Bitmap *QACreateBitmap(long BitmapSize)
{
   Bitmap *BmapPtr;
   long ByteLen;

   BmapPtr=(Bitmap *)malloc(sizeof(Bitmap));
   if(BmapPtr==NULL) return(NULL);

   ByteLen=(BitmapSize/8)+1;

   BmapPtr->MapPtr=(char *)malloc(ByteLen);
   if(BmapPtr==NULL) {
      free(BmapPtr);
      return(NULL);
      }

   BmapPtr->MapLen=BitmapSize;
   memset(BmapPtr->MapPtr,0,ByteLen);

   return(BmapPtr);
   } /* end: CreateBitmap() */

/***********************************************************************
** FreeBitmap()
**
** This function frees the space allocated by CreateBitmap()
************************************************************************/
void FreeBitmap(Bitmap *BitmapPtr)
{
   free(BitmapPtr->MapPtr);
   free(BitmapPtr);
   } /* end: FreeBitmap() */


/***********************************************************************
** SetBit()
** This function will set the bit specified in <BitPosition> to either
** ON or OFF depending on which was specified in the function call.
**
** Inputs: bit setting (either ON or OFF, 1 or 0)
**         pointer to bitmap
**         bit position to be set
** Returns: void
************************************************************************/
void SetBit(int Flag,Bitmap *BitmapPtr,long BitPosition)
{
   long BitOffset;
   long ByteOffset;
   char *BmapPtr;
   ByteOffset=BitPosition/8;
   BitOffset=BitPosition%8;
   BmapPtr=BitmapPtr->MapPtr;
   BmapPtr+=ByteOffset;
   if(Flag!=BIT_OFF){
      *BmapPtr|=byte_mask[BitOffset];    /* turn bit on */
      }
   else{
      *BmapPtr^=0xff;                    /* turn bit off */
      *BmapPtr|=byte_mask[BitOffset];
      *BmapPtr^=0xff;
      }
   } /* end: SetBit() */

/***********************************************************************
** SetBitBlock()
** This function will set the block of bits starting at <BitPosition> to
** ON or OFF depending on which was specified in the function call.  If
** the block size goes beyond the end of the bitmap, then it is
** automatically wrapped around to the beginning of the bitmap.
**
** Inputs: bit setting (either ON or OFF, 1 or 0)
**         pointer to bitmap
**         bit position to be set
**         size of block (in bits)
** Returns: void
************************************************************************/
void SetBitBlock(int Flag,Bitmap *BitmapPtr,long BitPosition,long BlockSize)
{
   long i;
   long LastBitPosition;

   LastBitPosition=BitPosition+BlockSize-1;
   if(LastBitPosition>BitmapPtr->MapLen){
      LastBitPosition-=BitmapPtr->MapLen;
      for(i=BitPosition;i<BitmapPtr->MapLen;i++){
         SetBit(Flag,BitmapPtr,i);
         }
      for(i=0;i<LastBitPosition;i++){
         SetBit(Flag,BitmapPtr,i);
         }
      }
   else {
      for(i=BitPosition;i<=LastBitPosition;i++){
         SetBit(Flag,BitmapPtr,i);
         }
      }
   } /* end: SetBitBlock() */

/***********************************************************************
** FindNextBit()
**
** Shell function for find_next_bit().
************************************************************************/
long FindNextBit(int flag,Bitmap *BmapPtr,long StartOffset,int SearchType)
{
   return(find_next_bit(flag,(bitmap *)BmapPtr->MapPtr,BmapPtr->MapLen,
                        StartOffset,SearchType));
   } /* end: FindNextBit() */

/***********************************************************************
** FindNextBitblock()
**
** Shell function for find_next_bitblock().
***********************************************************************/
long FindNextBitBlock(int Flag, Bitmap *BmapPtr,
                      long StartOffset,int SearchType,
                      long RequestedBlockSize,long *ActualBlockSize){

	return(find_next_bitblock(Flag,(bitmap *)BmapPtr->MapPtr,BmapPtr->MapLen,
                        StartOffset,SearchType,RequestedBlockSize,
                        ActualBlockSize));
   }


/***********************************************************************
** CountBits()
**
** This function will count the number of bits (either ON or OFF bits
** can be counted)
**
** Inputs: bit setting to count
**         pointer to Bitmap
**
** Returns: count of bits
************************************************************************/
long CountBits(int Flag,Bitmap *BitmapPtr)
{
   long BitOffset;
   char *Ptr;
   long Offset;
   long BitCount;
   char TempChar;

   BitCount=0;
   Offset=0;
   BitOffset=0;
   Ptr=BitmapPtr->MapPtr;

   /* count until end of bitmap is reached */
   while(Offset<BitmapPtr->MapLen){
      while((BitOffset<8)&&(Offset<BitmapPtr->MapLen)){
         TempChar=*Ptr&byte_mask[BitOffset];
         if(((Flag==BIT_OFF)&&(TempChar==0))||
            ((Flag==BIT_ON)&&(TempChar!=0))){
               BitCount++;
               }
         Offset++;
         BitOffset++;
         }
      Ptr++;
      BitOffset=0;
      }

   return(BitCount);
   } /* end: CountBits() */

/***********************************************************************
** CopyBitmap()
**
** This function will copy one Bitmap structure to another.  The TO bitmap
** needs to be created prior to calling this function.
**
** Inputs: Pointer to TO Bitmap
**         pointer to FROM Bitmap
**
** Returns: nothing, however will generate an "assert" if either bitmap pointer
**          is NULL when function is called.
************************************************************************/
void CopyBitmap(Bitmap *pToBitmap, Bitmap *pFromBitmap)
{
	// check bitmap pointers
	assert(pToBitmap!=NULL);
	assert(pFromBitmap!=NULL);

	// Copy the bitmap structure
	pToBitmap->MapLen=pFromBitmap->MapLen;
	memcpy(pToBitmap->MapPtr,pFromBitmap->MapPtr,(pFromBitmap->MapLen/8)+1);

}
