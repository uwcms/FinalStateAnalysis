#ifndef HIGGSCSANDWIDTHFERMI_H
#define HIGGSCSANDWIDTHFERMI_H

#define PI 3.14159

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
/*       Last Update: July 6, 2011                        */
/*                                                        */
/**********************************************************/



class HiggsCSandWidthFermi
{

 public:

  HiggsCSandWidthFermi();
  ~HiggsCSandWidthFermi();

  double HiggsWidth(int ID,double mH);


 private:

  double scratchMass;
  double BR[12][681];

  std::string FileLoc;


};

#endif
