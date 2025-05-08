/* ****************************************************************** **
**    OpenSees - Open System for Earthquake Engineering Simulation    **
**          Pacific Earthquake Engineering Research Center            **
**                                                                    **
**                                                                    **
** (C) Copyright 1999, The Regents of the University of California    **
** All Rights Reserved.                                               **
**                                                                    **
** Commercial use of this program without express permission of the   **
** University of California, Berkeley, is strictly prohibited.  See   **
** file 'COPYRIGHT'  in main directory for information on usage and   **
** redistribution,  and for a DISCLAIMER OF ALL WARRANTIES.           **
**                                                                    **
** Developed by:                                                      **
**   Frank McKenna (fmckenna@ce.berkeley.edu)                         **
**   Gregory L. Fenves (fenves@ce.berkeley.edu)                       **
**   Filip C. Filippou (filippou@ce.berkeley.edu)                     **
**                                                                    **
** ****************************************************************** */
//
// Description: This file contains the class definition for 
// UmfpackGenLinSolver. It solves the UmfpackGenLinSOEobject by calling
// UMFPACK5.7.1 routines.
//
// Written: fmk 
// Created: 11/98
//
#ifndef UmfpackGenLinSolver_h
#define UmfpackGenLinSolver_h

#include <LinearSOESolver.h>
#include "../../../../OTHER/UMFPACK/umfpack.h"

class UmfpackGenLinSOE;

class UmfpackGenLinSolver : public LinearSOESolver
{
  public:
    UmfpackGenLinSolver(bool doDet = false);     
    ~UmfpackGenLinSolver();

    int solve(void);
    int setSize(void);

    int setLinearSOE(UmfpackGenLinSOE &theSOE);
    
    int sendSelf(int commitTag, Channel &theChannel);
    int recvSelf(int commitTag, Channel &theChannel, 
		 FEM_ObjectBroker &theBroker);    

    virtual double getDeterminant() override;
    
  protected:

  private:
    void *Symbolic;
    double Control[UMFPACK_CONTROL], Info[UMFPACK_INFO];
    UmfpackGenLinSOE *theSOE;
    double det;
    bool doDet;
};

#endif

