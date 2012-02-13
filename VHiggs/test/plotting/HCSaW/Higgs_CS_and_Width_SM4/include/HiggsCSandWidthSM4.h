#ifndef HIGGSCSANDWIDTHSM4_H
#define HIGGSCSANDWIDTHSM4_H

#define PI 3.14159

#define  ID_ggToH  1
#define  ID_VBF    2
#define  ID_WH     3
#define  ID_ZH     4
#define  ID_ttH    5
#define  ID_Total  0 

#include <iostream>
#include <cstdlib>
#include <cmath>
#include <fstream>
#include <string>


/**********************************************************/
/*            Class for Higgs Width and CS                */
/*                                                        */
/*  All numbers for CS and width are taken from official  */
/*  numbers on Higgs CS Twiki (Spring 2011)               */
/*                                                        */
/*  Cross Sections are given in pb                        */
/*  Widths are given in GeV                               */
/*                                                        */
/*  These numbers are taken into memory and a simple      */
/*  linear interpolation is done.                         */
/*                                                        */
/*  For any invalid process or mH out of range, -1 will   */
/*  be returned.                                          */
/*                                                        */
/*    Written by:                                         */
/*         Matt Snowball                                  */
/*         University of Florida                          */
/*         snowball@phys.ufl.edu                          */
/*                                                        */
/*       Last Update: Feb 6, 2012                         */
/*                                                        */
/**********************************************************/



class HiggsCSandWidthSM4
{

 public:

  HiggsCSandWidthSM4();
  ~HiggsCSandWidthSM4();

  double HiggsCS(int ID, double mH, double sqrts);
  double HiggsCSErrPlus(int ID, double mH, double sqrts);
  double HiggsCSErrMinus(int ID, double mH, double sqrts);
  double HiggsCSscaleErrPlus(int ID, double mH, double sqrts);
  double HiggsCSscaleErrMinus(int ID, double mH, double sqrts);
  double HiggsCSpdfErrPlus(int ID, double mH, double sqrts);
  double HiggsCSpdfErrMinus(int ID, double mH, double sqrts);

  double HiggsWidth(int ID,double mH);


 private:

  double scratchMass;
  double BR[18][102];
  double CS[6][109];
  double CSerrPlus[6][175];
  double CSerrMinus[6][175];
  double CSscaleErrPlus[6][175];
  double CSscaleErrMinus[6][175];
  double CSpdfErrPlus[6][175];
  double CSpdfErrMinus[6][175];


  std::string FileLoc;


};

#endif
