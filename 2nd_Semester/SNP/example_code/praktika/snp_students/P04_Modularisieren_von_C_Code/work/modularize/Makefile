SNP_SHARED_MAKEFILE := $(if $(SNP_SHARED_MAKEFILE),$(SNP_SHARED_MAKEFILE),~/snp/shared.mk)

TARGET     := bin/triangle
SOURCES    := src/triangle.c src/read.c src/rectang.c
TSTSOURCES := tests/tests.c
LIBS       := -lm

include $(SNP_SHARED_MAKEFILE)
