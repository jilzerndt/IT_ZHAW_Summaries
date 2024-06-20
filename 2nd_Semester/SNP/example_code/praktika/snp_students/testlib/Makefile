# what to produce
TARGET        := lib/libsnptest.a

# public headers
HEADERS       := include/test_utils.h

# implementation files
SOURCES       := src/test_utils.c

# test implementations
TSTSOURCES    := tests/tests.c

# directories to create (and remove upon cleanup)
CREATEDIRS    := lib doc

# list of derived file names from the source names
OBJECTS       := $(SOURCES:%.c=%.o)    # list of gcc -c  ... produced *.o files
DEPS          := $(SOURCES:%.c=%.d)    # list of gcc -MD ... produced *.d files
TSTOBJECTS    := $(TSTSOURCES:%.c=%.o) # list of gcc -c  ... produced *.o files
TSTDEPS       := $(TSTSOURCES:%.c=%.d) # list of gcc -MD ... produced *.d files
TSTTARGET     := $(CURDIR)/tests/runtest

# full path to the target
FULLTARGET    := $(CURDIR)/$(TARGET)

# commands and flags
CC            = gcc
CFLAGS        = -std=c99 -Wall -pedantic -g
CPPFLAGS      = -MD -Isrc -Itests -Iinclude -DTARGET=$(FULLTARGET)
LDFLAGS       = 
ARFLAGS       = rc

# targets which get always visited (without checking any up-to-date state)
.PHONY: default clean test doc install mkdir

# targets
default: $(FULLTARGET)
	@echo "#### $< built ####"

$(FULLTARGET): mkdir $(OBJECTS) Makefile
	$(AR) $(ARFLAGS) $@ $(OBJECTS)

clean:
	$(RM) $(TARGET) $(OBJECTS) $(DEPS) $(TSTTARGET) $(TSTOBJECTS) $(TSTDEPS) $(wildcard */*~ *~ tests/*.txt)
	$(RM) -r $(CREATEDIRS)
	@echo "#### $@ done ####"

install: $(FULLTARGET)
	@echo "#### $< installed ####"

doc:
	doxygen ../Doxyfile > /dev/null
	@echo "#### $@ done ####"

test: $(TSTTARGET)
	(cd tests; $(TSTTARGET))
	@echo "#### $< executed ####"

$(TSTTARGET): $(FULLTARGET) $(TSTOBJECTS)
	$(LINK.c) -o $(TSTTARGET) $(TSTOBJECTS) $(FULLTARGET) -lcunit
	@echo "#### $@ built ####"


# create needed directories (ignoring any error)
mkdir:
	-mkdir -p $(CREATEDIRS)

# read in the gcc -MD ... produced dependencies (ignoring any error)
-include $(DEPS) $(TSTDEPS)
