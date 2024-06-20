EMPTY      :=
SPACE      := $(EMPTY) $(EMPTY)
NL         := $(EMPTY)\\n$(EMPTY)

LABS       := $(sort $(wildcard P[0-9][0-9]*))
EXAMPLE    := $(if $(firstword $(LABS)),$(firstword $(LABS)),"Pxx")

default:
	@echo "**** SNP Labs ****"
	@echo "$(subst $(SPACE),$(NL),$(LABS))"
	@echo ""
	@echo "**** Prerequisites ****"
	@echo "1. Change into the testlib directory"
	@echo "       cd testlib"
	@echo "2. Build and install the library, e.g."
	@echo "       make clean"
	@echo "       make default"
	@echo "       make test"
	@echo "       make install"
	@echo "   Caution: make sure the tests and installation does not produce any error."
	@echo ""
	@echo "**** How to build and run a lab? ****"
	@echo "1. Change into the respective directory, e.g."
	@echo "       cd $(EXAMPLE)"
	@echo "2. Build the lab, e.g."
	@echo "       make"
	@echo "   The resulting executable is located in the bin folder."
	@echo "3. Build and run the tests, e.g."
	@echo "       make test"
	@echo "Notes:"
	@echo "- You may cleanup the builds, e.g."
	@echo "       make clean"
