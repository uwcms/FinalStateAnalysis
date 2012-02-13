#ifndef HIGGSCSANDWIDTHFERMI_CC
#define HIGGSCSANDWIDTHFERMI_CC


#include <iostream>
#include <cmath>
#include <string>
#include <cstdlib>
#include <fstream>

#include "HiggsCSandWidthFermi.h"

using namespace std;

HiggsCSandWidthFermi::HiggsCSandWidthFermi()
{


  ifstream file;
 
  // Read Widths into memory
  FileLoc = "../txtFiles/Higgs_BR_Fermiophobic.txt"; //directory of input file
  const char* BranchRatioFileLoc = FileLoc.c_str(); 
  file.open(BranchRatioFileLoc);
  for(int k = 0; k < 681; k++){

    file >> scratchMass >> BR[7][k] >> BR[8][k] >> BR[9][k] >> BR[10][k] >> BR[11][k] >> BR[0][k];


  }
  file.close();


}


HiggsCSandWidthFermi::~HiggsCSandWidthFermi()
{
  //destructor

}


// HiggsWidth takes process ID and higgs mass mH
double HiggsCSandWidthFermi::HiggsWidth(int ID, double mH){


  /***********************IDs************************/
  /*                       Total = 0                */
  /*                   H->gamgam = 8                */
  /*                     H->gamZ = 9                */
  /*                       H->WW = 10               */
  /*                       H->ZZ = 11               */
  /**************************************************/



  double TotalWidth = 0;
  double PartialWidth = 0;
  double Width = 0;
  int i = 0;
  double closestMass = 0;
  double tmpLow1, tmpHigh1, deltaX, deltaY1, slope1;
  double deltaY2, tmpLow2, tmpHigh2, slope2, step;


  // If ID is unavailable return -1                                           
  if((ID > 11 || ID < 8) && ID != 0){return 0;}


  // If mH is out of range return -1                                            
  // else find what array number to read                                        
  if( mH < 80 || mH > 250){return 0;}
  else{

    //Find index and closest higgs mass for which we have numbers
    step = 0.25; i = (int)((mH - 80)/step); closestMass = (double)(step*i + 80);
    
      tmpLow1 = BR[ID][i]*BR[0][i];                                                                                                                        
      tmpHigh1 = BR[ID][i+1]*BR[0][i+1];                                                                                                                   


      tmpLow2 = BR[0][i];
      tmpHigh2 = BR[0][i+1];
      deltaX = mH - closestMass;

      deltaY1 = tmpHigh1 - tmpLow1;
      slope1 = deltaY1/step;


      deltaY2 = tmpHigh2 - tmpLow2;
      slope2 = deltaY2/step;


      // For partial widths                                                                                                                 
      if(deltaX == 0){ PartialWidth = tmpLow1;
	TotalWidth = tmpLow2;}
      else{ PartialWidth = slope1*deltaX + tmpLow1;
	TotalWidth = slope2*deltaX + tmpLow2;}

      // For total width  
      if( ID == 0 ){ Width = TotalWidth; }
      else{ Width = PartialWidth;}

  }

  return Width;

} 





#endif
