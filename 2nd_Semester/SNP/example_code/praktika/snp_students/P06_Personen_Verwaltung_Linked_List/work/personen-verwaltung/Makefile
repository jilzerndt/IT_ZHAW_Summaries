SNP_SHARED_MAKEFILE := $(if $(SNP_SHARED_MAKEFILE),$(SNP_SHARED_MAKEFILE),~/snp/shared.mk)

TARGET     := bin/personen-verwaltung
# BEGIN-STUDENTS-TO-ADD-CODE
MODULES    := src/person.c src/list.c
# END-STUDENTS-TO-ADD-CODE
SOURCES    := src/main.c $(MODULES)
TSTSOURCES := tests/tests.c $(MODULES)


include $(SNP_SHARED_MAKEFILE)

# CFLAGS  += -Werror
