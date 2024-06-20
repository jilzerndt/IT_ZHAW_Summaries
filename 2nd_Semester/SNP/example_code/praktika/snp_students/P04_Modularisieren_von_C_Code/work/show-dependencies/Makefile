SNP_SHARED_MAKEFILE := $(if $(SNP_SHARED_MAKEFILE),$(SNP_SHARED_MAKEFILE),~/snp/shared.mk)

TARGET     := bin/dep2dot
# Add all additional c-files to the SOURCES variable
# BEGIN-STUDENTS-TO-ADD-CODE
SOURCES    := src/main.c src/data.c src/output.c
# END-STUDENTS-TO-ADD-CODE
TSTSOURCES := tests/tests.c

include $(SNP_SHARED_MAKEFILE)


# DEPFILES :=  ... define a list of png file names: %.c -> %.c.png
# BEGIN-STUDENTS-TO-ADD-CODE
DEPFILES := $(SOURCES:%.c=%.c.png)


# END-STUDENTS-TO-ADD-CODE



# define dep target as .PHONEY
# BEGIN-STUDENTS-TO-ADD-CODE
.PHONEY: dep

# BEGIN-STUDENTS-TO-ADD-CODE



# define dep target depending on FULLTARGET and DEPFILES above
# action: echo some text telling that the target is done using $@ - the echo command shall not be echoed before execution
# BEGIN-STUDENTS-TO-ADD-CODE
dep: $(FULLTARGET) $(DEPFILES)
	@echo "dep done using $@"


# BEGIN-STUDENTS-TO-ADD-CODE



# define new suffix rule for %.png depending on %.dot
# action: dot -Tpng $< >$@ || $(RM) $@
# BEGIN-STUDENTS-TO-ADD-CODE
%.png: %.dot
	dot -Tpng $< >$@ || $(RM) $@

# BEGIN-STUDENTS-TO-ADD-CODE



# define new suffix rule for %.dot depending on %.dep
# action: call $(TARGET) $(@:.dot=) <$< >$@ || $(RM) $@
# BEGIN-STUDENTS-TO-ADD-CODE
%.dot: %.dep
	$(TARGET) $(@:.dot=) <$< >$@ || $(RM) $@


# BEGIN-STUDENTS-TO-ADD-CODE



# converts any .c file into a .c.dep file by means of GCC -H switch
# note: it removes intermediate files which were created as side effect
%.c.dep: %.c
	$(COMPILE.c) -H -o $@.x $< 2>$@ && $(RM) $@.x $@.d


# cleanup all results, including the ones od creating the dependencies
dep-clean: clean
	$(RM) $(DEPFILES) $(wildcard src/*.dep src/*.dot)

