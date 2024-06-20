//******************************************************************************
// Course:  BSy
// File:    banking.h
// Author:  M. Thaler, ZHAW
// Purpose: locking mechanisms
// Version: v.fs20
//******************************************************************************
// banking functions

void makeBank(int num_branches, int num_accounts);
void deleteBank(void);

long int withdraw(int branchNr, int accountNr, long int value) ;
void deposit(int branchNr, int accountNr, long int value);
void transfer(int fromB, int toB, int accountNr, long int value);
void checkAssets(void);

//******************************************************************************

