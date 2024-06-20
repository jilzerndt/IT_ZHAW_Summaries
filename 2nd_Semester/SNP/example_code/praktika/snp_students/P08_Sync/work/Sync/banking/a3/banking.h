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

long withdraw(int branch, int account, long int value) ;
void deposit(int branch, int account, long int value);
void transfer(int fromB, int toB, int account, long int value);
void checkAssets(void);
int  checkIBC(void);

//******************************************************************************

