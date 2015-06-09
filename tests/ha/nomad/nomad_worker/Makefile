#------------------------------------------------
# Makefile to create QA's libraries
#------------------------------------------------

# distribution directories
DISTROOT = $(PWD)
OBJ = $(DISTROOT)/obj
#------------------------------------------------

CREATE_PATH ?= mkdir -p $(@D)

SRC = .
INCDIRS =	-I $(SRC) -I /usr/include -I /usr/include/odbc \
            -I $(SRC)/../qalib

TARGETS =	$(SRC)/NomadWorker

CPP_COMPILER = g++
C_FLAGS = -O0 -g -DDEBUG -DNA_LINUX -fPIC -Wno-write-strings
CPP_FLAGS = $(C_FLAGS)
LIBDIRS = -L $(SRC)/../qalib/lib -L /usr/lib64 -L /h/andersma/odbc
LIBS = -l trafodbc64 -l qa -l icuucNv44 -l icudataNv44
LINK_FLAGS =

C_COMPILE_LINK		= gcc -o $@ $(C_FLAGS) $(INCDIRS) $(LIBDIRS) $(LIBS)
CPP_COMPILE_LINK	= $(CPP_COMPILER) $(CPP_FLAGS) -o $@  $(INCDIRS) $(LIBDIRS) $(LIBS) \
					-L $(LIB) $<
C_COMPILE_ONLY    = gcc -c -o $@ $(C_FLAGS) $(INCDIRS) $<
CPP_COMPILE_ONLY  = $(CPP_COMPILER) -c -o $@ $(CPP_FLAGS) $(INCDIRS) $<

LINK_SHARED_LIB = $(CPP_COMPILER) -shared -o $@ $(LINK_FLAGS) $(LIBDIRS) $(LIBS)

#---------------------------------------------------
all: $(TARGETS)

# build the executable
$(SRC)/NomadWorker: \
   $(SRC)/../qalib/lib/libqa.so \
	$(OBJ)/delete.o \
	$(OBJ)/getcmds.o \
	$(OBJ)/insert.o \
	$(OBJ)/main.o \
	$(OBJ)/main2.o \
	$(OBJ)/select.o \
	$(OBJ)/sqlutil2.o \
	$(OBJ)/status.o \
	$(OBJ)/update.o
		@$(CREATE_PATH)
		@echo '*** Compile and Link $(@F) ***'
		@$(C_COMPILE_LINK) \
			$(OBJ)/delete.o $(OBJ)/getcmds.o $(OBJ)/insert.o \
			$(OBJ)/main.o $(OBJ)/main2.o $(OBJ)/select.o \
			$(OBJ)/sqlutil2.o $(OBJ)/status.o $(OBJ)/update.o

# compile all the object files
$(OBJ)/delete.o: $(SRC)/delete.c $(SRC)/sqlutil2.h
		@$(CREATE_PATH)
		@echo '*** Compiling $(<F) ***'
		@$(C_COMPILE_ONLY)

$(OBJ)/getcmds.o: $(SRC)/getcmds.c
		@$(CREATE_PATH)
		@echo '*** Compiling $(<F) ***'
		@$(C_COMPILE_ONLY)

$(OBJ)/insert.o: $(SRC)/insert.c $(SRC)/sqlutil2.h
		@$(CREATE_PATH)
		@echo '*** Compiling $(<F) ***'
		@$(C_COMPILE_ONLY)

$(OBJ)/main.o: $(SRC)/main.c $(SRC)/globals.c $(SRC)/status.h
		@$(CREATE_PATH)
		@echo '*** Compiling $(<F) ***'
		@$(C_COMPILE_ONLY)

$(OBJ)/main2.o: $(SRC)/main2.c $(SRC)/status.h
		@$(CREATE_PATH)
		@echo '*** Compiling $(<F) ***'
		@$(C_COMPILE_ONLY)

$(OBJ)/select.o: $(SRC)/select.c
		@$(CREATE_PATH)
		@echo '*** Compiling $(<F) ***'
		@$(C_COMPILE_ONLY)

$(OBJ)/sqlutil2.o: $(SRC)/sqlutil2.c
		@$(CREATE_PATH)
		@echo '*** Compiling $(<F) ***'
		@$(C_COMPILE_ONLY)

$(OBJ)/status.o: $(SRC)/status.c
		@$(CREATE_PATH)
		@echo '*** Compiling $(<F) ***'
		@$(C_COMPILE_ONLY)

$(OBJ)/update.o: $(SRC)/update.c
		@$(CREATE_PATH)
		@echo '*** Compiling $(<F) ***'
		@$(C_COMPILE_ONLY)


# >>>This should be replaced by automatically generating dependence
# >>>files using some form of the follow:
# >>>CC_DEPEND_IT     = cd $(@D); $(CC_CC) -WM $(CC_CFLAGS) $(ALL_INCLUDEDIR_LIST) \
# >>>                   $< | sed -e 's@\(.*\)/.o:@$(@D)/\1.o $(@D)/\1.d:@' >$@

#---------------------------------------------------
clean:
	@echo '***** Cleaning *****'
	-rm $(SRC)/NomadWorker \
	$(OBJ)/delete.o \
	$(OBJ)/getcmds.o \
	$(OBJ)/insert.o \
	$(OBJ)/main.o \
	$(OBJ)/main2.o \
	$(OBJ)/select.o \
	$(OBJ)/sqlutil2.o \
	$(OBJ)/status.o \
	$(OBJ)/update.o
		