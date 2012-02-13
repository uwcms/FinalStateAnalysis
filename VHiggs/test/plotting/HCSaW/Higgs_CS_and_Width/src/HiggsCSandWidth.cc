#ifndef HIGGSCSANDWIDTH_CC
#define HIGGSCSANDWIDTH_CC


#include <iostream>
#include <cmath>
#include <string>
#include <cstdlib>
#include <fstream>

#include "HiggsCSandWidth.h"

using namespace std;

HiggsCSandWidth::HiggsCSandWidth()
{


  ifstream file;
 
  // Read Widths into memory
  FileLoc = "../txtFiles/HiggsBR_7TeV_Official.txt"; //directory of input file
  const char* BranchRatioFileLoc = FileLoc.c_str(); 
  file.open(BranchRatioFileLoc);
  for(int k = 0; k < 217; k++){

    file >> scratchMass >> BR[0][k] >> BR[1][k] >> BR[2][k] >> BR[3][k] >> BR[4][k] >> BR[5][k] >> BR[6][k] >> BR[7][k] >> BR[8][k] >> BR[9][k]
	 >> BR[10][k] >> BR[11][k] >> BR[12][k] >> BR[13][k] >> BR[14][k] >> BR[15][k] >> BR[16][k] >> BR[17][k] >> BR[18][k] >> BR[19][k] >> BR[20][k]
	 >> BR[21][k] >> BR[22][k] >> BR[23][k] >> BR[24][k] >> BR[25][k];


  }
  file.close();

  // Read CS into memory                                                                                                                                                  
  file.open("../txtFiles/HiggsCS_Official.txt");//directory of input file
  for(int k = 0; k < 197; k++){

    file >> scratchMass >> CS[ID_ggToH][k] >> CS[ID_VBF][k] >> CS[ID_WH][k] >> CS[ID_ZH][k] >> CS[ID_ttH][k] >> CS[ID_Total][k];

  }
  file.close();

  file.open("../txtFiles/HiggsCS_ErrorPlus_Official.txt");//directory of input file                       
  for(int k = 0; k < 197; k++){

    file >> scratchMass >> CSerrPlus[ID_ggToH][k] >> CSerrPlus[ID_VBF][k] >> CSerrPlus[ID_WH][k] >> CSerrPlus[ID_ZH][k] >> CSerrPlus[ID_ttH][k];

  }
  file.close();

  file.open("../txtFiles/HiggsCS_ErrorMinus_Official.txt");//directory of input file                                                
  for(int k = 0; k < 197; k++){

    file >> scratchMass >> CSerrMinus[ID_ggToH][k] >> CSerrMinus[ID_VBF][k] >> CSerrMinus[ID_WH][k] >> CSerrMinus[ID_ZH][k] >> CSerrMinus[ID_ttH][k];

  }
  file.close();

  file.open("../txtFiles/HiggsCS_ScaleErrorPlus_Official.txt");//directory of input file                                                
  for(int k = 0; k < 197; k++){

    file >> scratchMass >> CSscaleErrPlus[ID_ggToH][k] >> CSscaleErrPlus[ID_VBF][k] >> CSscaleErrPlus[ID_WH][k] >> CSscaleErrPlus[ID_ZH][k] >> CSscaleErrPlus[ID_ttH][k];

  }
  file.close();

  file.open("../txtFiles/HiggsCS_ScaleErrorMinus_Official.txt");//directory of input file                                     
  for(int k = 0; k < 197; k++){

    file >> scratchMass >> CSscaleErrMinus[ID_ggToH][k] >> CSscaleErrMinus[ID_VBF][k] >> CSscaleErrMinus[ID_WH][k] >> CSscaleErrMinus[ID_ZH][k] >> CSscaleErrMinus[ID_ttH][k];

  }
  file.close();

  file.open("../txtFiles/HiggsCS_PdfErrorPlus_Official.txt");//directory of input file                  
  for(int k = 0; k < 197; k++){

    file >> scratchMass >> CSpdfErrPlus[ID_ggToH][k] >> CSpdfErrPlus[ID_VBF][k] >> CSpdfErrPlus[ID_WH][k] >> CSpdfErrPlus[ID_ZH][k] >> CSpdfErrPlus[ID_ttH][k];

  }
  file.close();

  file.open("../txtFiles/HiggsCS_PdfErrorMinus_Official.txt");//directory of input file                           
  for(int k = 0; k < 197; k++){

    file >> scratchMass >> CSpdfErrMinus[ID_ggToH][k] >> CSpdfErrMinus[ID_VBF][k] >> CSpdfErrMinus[ID_WH][k] >> CSpdfErrMinus[ID_ZH][k] >> CSpdfErrMinus[ID_ttH][k];

  }
  file.close();

}


HiggsCSandWidth::~HiggsCSandWidth()
{
  //destructor

}


//Higgs CS takes process ID, higgs mass mH, and COM energy sqrts in TeV (numbers are for 7 TeV only in this version)
double HiggsCSandWidth::HiggsCS(int ID, double mH, double sqrts){

  /**********IDs*************/ 
  /*     ggToH = 1          */
  /*       VBF = 2          */ 
  /*        WH = 3          */ 
  /*        ZH = 4          */
  /*       ttH = 5          */
  /*     Total = 0          */
  /**************************/
 
  int i = 0;
  double closestMass = 0;
  double reqCS = 0;
  double tmpLow = 0, tmpHigh = 0;
  double deltaX = 0, deltaY = 0;
  double slope = 0;
  double step = 0;


  // If ID is unavailable return -1                                                                                                
  if(ID > ID_ttH || ID < ID_Total){return -1;}
  // If Ecm is not 7 TeV return -1
  if(sqrts != 7){return -1;}
  //Don't interpolate btw 0 and numbers for mH300
  if(ID > ID_VBF && mH > 300){return 0;}


  // If mH is out of range return -1                                           
  // else find what array number to read         
  if( mH < 90 || mH > 1000){return -1;}
  else{

    if(mH <= 110 ){step = 5; i = (int)((mH - 90)/step); closestMass = (int)(step*i + 90);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(4 + (mH - 110)/step); closestMass = (step*(i-4) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(64 + (mH - 140)/step); closestMass = (int)(step*(i-64) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(84 + (mH - 160)/step); closestMass = (int)(step*(i-84) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(149 + (mH - 290)/step); closestMass = (int)(step*(i-149) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(161 + (mH-350)/step); closestMass = (int)(step*(i-161) + 350);}
    if(mH > 400){step = 20; i = (int)(166 + (mH-400)/step); closestMass = (int)(step*(i-166) + 400);}

      tmpLow = CS[ID][i];
      tmpHigh = CS[ID][i+1];

      deltaX = mH - closestMass;

      deltaY = tmpHigh - tmpLow;
      slope = deltaY/step;

      // For partial widths   
      if(deltaX == 0){ reqCS = tmpLow;}
      else{ reqCS = slope*deltaX + tmpLow;}

    }

  return reqCS;

}


//Higgs CS takes process ID, higgs mass mH, and COM energy sqrts in TeV (numbers are for 7 TeV only in this version)                   
double HiggsCSandWidth::HiggsCSErrPlus(int ID, double mH, double sqrts){

  /**********IDs*************/
  /*     ggToH = 1          */
  /*       VBF = 2          */
  /*        WH = 3          */
  /*        ZH = 4          */
  /*       ttH = 5          */
  /**************************/

  int i = 0;
  double closestMass = 0;
  double reqCSerr = 0;
  double tmpLow = 0, tmpHigh = 0;
  double deltaX = 0, deltaY = 0;
  double slope = 0;
  double step = 0;


  // If ID is unavailable return -1                                                                                    
  if(ID > ID_ttH || ID < ID_Total){return -1;}
  if(ID == ID_Total){return 0;}
  // If Ecm is not 7 TeV return -1                                                                                                
  if(sqrts != 7){return -1;}
  //Don't interpolate btw 0 and numbers for mH300                        
  if(ID > ID_VBF && mH > 300){return 0;}

  // If mH is out of range return -1                                                                        
  // else find what array number to read                                          
  if( mH < 90 || mH > 1000){return -1;}
  else{

    if(mH <= 110 ){step = 5; i = (int)((mH - 90)/step); closestMass = (int)(step*i + 90);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(4 + (mH - 110)/step); closestMass = (step*(i-4) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(64 + (mH - 140)/step); closestMass = (int)(step*(i-64) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(84 + (mH - 160)/step); closestMass = (int)(step*(i-84) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(149 + (mH - 290)/step); closestMass = (int)(step*(i-149) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(161 + (mH-350)/step); closestMass = (int)(step*(i-161) + 350);}
    if(mH > 400){step = 20; i = (int)(166 + (mH-400)/step); closestMass = (int)(step*(i-166) + 400);}



    tmpLow = CSerrPlus[ID][i];
    tmpHigh = CSerrPlus[ID][i+1];

    deltaX = mH - closestMass;

    deltaY = tmpHigh - tmpLow;
    slope = deltaY/step;

    // For partial widths                                                                                                      
    if(deltaX == 0){ reqCSerr = tmpLow;}
    else{ reqCSerr = slope*deltaX + tmpLow;}
    reqCSerr *= .01; //Account for percentage
  }

  return reqCSerr;

}


//Higgs CS takes process ID, higgs mass mH, and COM energy sqrts in TeV (numbers are for 7 TeV only in this version)      
double HiggsCSandWidth::HiggsCSErrMinus(int ID, double mH, double sqrts){

  /**********IDs*************/
  /*     ggToH = 1          */
  /*       VBF = 2          */
  /*        WH = 3          */
  /*        ZH = 4          */
  /*       ttH = 5          */
  /**************************/

  int i = 0;
  double closestMass = 0;
  double reqCSerr = 0;
  double tmpLow = 0, tmpHigh = 0;
  double deltaX = 0, deltaY = 0;
  double slope = 0;
  double step = 0;


  // If ID is unavailable return -1                                                                                       
  if(ID > ID_ttH || ID < ID_Total){return -1;}
  if(ID == ID_Total){return 0;}
  // If Ecm is not 7 TeV return -1                                                                                           
  if(sqrts != 7){return -1;}
  //Don't interpolate btw 0 and numbers for mH300                                                        
  if(ID > ID_VBF && mH > 300){return 0;}


  // If mH is out of range return -1                                                                           
  // else find what array number to read                                                                 
  if( mH < 90 || mH > 1000){return -1;}
  else{

    if(mH <= 110 ){step = 5; i = (int)((mH - 90)/step); closestMass = (int)(step*i + 90);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(4 + (mH - 110)/step); closestMass = (step*(i-4) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(64 + (mH - 140)/step); closestMass = (int)(step*(i-64) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(84 + (mH - 160)/step); closestMass = (int)(step*(i-84) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(149 + (mH - 290)/step); closestMass = (int)(step*(i-149) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(161 + (mH-350)/step); closestMass = (int)(step*(i-161) + 350);}
    if(mH > 400){step = 20; i = (int)(166 + (mH-400)/step); closestMass = (int)(step*(i-166) + 400);}



    tmpLow = CSerrMinus[ID][i];
    tmpHigh = CSerrMinus[ID][i+1];

    deltaX = mH - closestMass;

    deltaY = tmpHigh - tmpLow;
    slope = deltaY/step;

    // For partial widths                                               
    if(deltaX == 0){ reqCSerr = tmpLow;}
    else{ reqCSerr = slope*deltaX + tmpLow;}
    reqCSerr *= .01; //Account for percentage                                                                                                   
  }

  return reqCSerr;

}

//Higgs CS takes process ID, higgs mass mH, and COM energy sqrts in TeV (numbers are for 7 TeV only in this version)          
double HiggsCSandWidth::HiggsCSscaleErrPlus(int ID, double mH, double sqrts){

  /**********IDs*************/
  /*     ggToH = 1          */
  /*       VBF = 2          */
  /*        WH = 3          */
  /*        ZH = 4          */
  /*       ttH = 5          */
  /**************************/

  int i = 0;
  double closestMass = 0;
  double reqCSerr = 0;
  double tmpLow = 0, tmpHigh = 0;
  double deltaX = 0, deltaY = 0;
  double slope = 0;
  double step = 0;


  // If ID is unavailable return -1                                                         
  if(ID > ID_ttH || ID < ID_Total){return -1;}
  if(ID == ID_Total){return 0;}
  // If Ecm is not 7 TeV return -1                                                
  if(sqrts != 7){return -1;}
  //Don't interpolate btw 0 and numbers for mH300                                           
  if(ID > ID_VBF && mH > 300){return 0;}

  // If mH is out of range return -1                                                         
  // else find what array number to read                                                      
  if( mH < 90 || mH > 1000){return -1;}
  else{

    if(mH <= 110 ){step = 5; i = (int)((mH - 90)/step); closestMass = (int)(step*i + 90);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(4 + (mH - 110)/step); closestMass = (step*(i-4) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(64 + (mH - 140)/step); closestMass = (int)(step*(i-64) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(84 + (mH - 160)/step); closestMass = (int)(step*(i-84) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(149 + (mH - 290)/step); closestMass = (int)(step*(i-149) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(161 + (mH-350)/step); closestMass = (int)(step*(i-161) + 350);}
    if(mH > 400){step = 20; i = (int)(166 + (mH-400)/step); closestMass = (int)(step*(i-166) + 400);}



    tmpLow = CSscaleErrPlus[ID][i];
    tmpHigh = CSscaleErrPlus[ID][i+1];

    deltaX = mH - closestMass;

    deltaY = tmpHigh - tmpLow;
    slope = deltaY/step;

    // For partial widths                                              
    if(deltaX == 0){ reqCSerr = tmpLow;}
    else{ reqCSerr = slope*deltaX + tmpLow;}
    reqCSerr *= .01; //Account for percentage                 
  }

  return reqCSerr;

}

//Higgs CS takes process ID, higgs mass mH, and COM energy sqrts in TeV (numbers are for 7 TeV only in this version)    
double HiggsCSandWidth::HiggsCSscaleErrMinus(int ID, double mH, double sqrts){

  /**********IDs*************/
  /*     ggToH = 1          */
  /*       VBF = 2          */
  /*        WH = 3          */
  /*        ZH = 4          */
  /*       ttH = 5          */
  /**************************/

  int i = 0;
  double closestMass = 0;
  double reqCSerr = 0;
  double tmpLow = 0, tmpHigh = 0;
  double deltaX = 0, deltaY = 0;
  double slope = 0;
  double step = 0;


  // If ID is unavailable return -1                     
  if(ID > ID_ttH || ID < ID_Total){return -1;}
  if(ID == ID_Total){return 0;}
  // If Ecm is not 7 TeV return -1                                                               
  if(sqrts != 7){return -1;}
  //Don't interpolate btw 0 and numbers for mH300                                   
  if(ID > ID_VBF && mH > 300){return 0;}


  // If mH is out of range return -1                        
  // else find what array number to read                              
  if( mH < 90 || mH > 1000){return -1;}
  else{

    if(mH <= 110 ){step = 5; i = (int)((mH - 90)/step); closestMass = (int)(step*i + 90);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(4 + (mH - 110)/step); closestMass = (step*(i-4) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(64 + (mH - 140)/step); closestMass = (int)(step*(i-64) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(84 + (mH - 160)/step); closestMass = (int)(step*(i-84) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(149 + (mH - 290)/step); closestMass = (int)(step*(i-149) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(161 + (mH-350)/step); closestMass = (int)(step*(i-161) + 350);}
    if(mH > 400){step = 20; i = (int)(166 + (mH-400)/step); closestMass = (int)(step*(i-166) + 400);}



    tmpLow = CSscaleErrMinus[ID][i];
    tmpHigh = CSscaleErrMinus[ID][i+1];

    deltaX = mH - closestMass;

    deltaY = tmpHigh - tmpLow;
    slope = deltaY/step;

    // For partial widths                                             
    if(deltaX == 0){ reqCSerr = tmpLow;}
    else{ reqCSerr = slope*deltaX + tmpLow;}
    reqCSerr *= .01; //Account for percentage                                                                                          
  }

  return reqCSerr;

}


//Higgs CS takes process ID, higgs mass mH, and COM energy sqrts in TeV (numbers are for 7 TeV only in this version)                  
double HiggsCSandWidth::HiggsCSpdfErrPlus(int ID, double mH, double sqrts){

  /**********IDs*************/
  /*     ggToH = 1          */
  /*       VBF = 2          */
  /*        WH = 3          */
  /*        ZH = 4          */
  /*       ttH = 5          */
  /**************************/

  int i = 0;
  double closestMass = 0;
  double reqCSerr = 0;
  double tmpLow = 0, tmpHigh = 0;
  double deltaX = 0, deltaY = 0;
  double slope = 0;
  double step = 0;


  // If ID is unavailable return -1                                                                           
  if(ID > ID_ttH || ID < ID_Total){return -1;}
  if(ID == ID_Total){return 0;}
  // If Ecm is not 7 TeV return -1                                                                                         
  if(sqrts != 7){return -1;}
  //Don't interpolate btw 0 and numbers for mH300                                                  
  if(ID > ID_VBF && mH > 300){return 0;}


  // If mH is out of range return -1                                                                                  
  // else find what array number to read                                                              
  if( mH < 90 || mH > 1000){return -1;}
  else{

    if(mH <= 110 ){step = 5; i = (int)((mH - 90)/step); closestMass = (int)(step*i + 90);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(4 + (mH - 110)/step); closestMass = (step*(i-4) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(64 + (mH - 140)/step); closestMass = (int)(step*(i-64) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(84 + (mH - 160)/step); closestMass = (int)(step*(i-84) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(149 + (mH - 290)/step); closestMass = (int)(step*(i-149) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(161 + (mH-350)/step); closestMass = (int)(step*(i-161) + 350);}
    if(mH > 400){step = 20; i = (int)(166 + (mH-400)/step); closestMass = (int)(step*(i-166) + 400);}



    tmpLow = CSpdfErrPlus[ID][i];
    tmpHigh = CSpdfErrPlus[ID][i+1];

    deltaX = mH - closestMass;

    deltaY = tmpHigh - tmpLow;
    slope = deltaY/step;

    // For partial widths                    
    if(deltaX == 0){ reqCSerr = tmpLow;}
    else{ reqCSerr = slope*deltaX + tmpLow;}
    reqCSerr *= .01; //Account for percentage                                                                                             
  }

  return reqCSerr;

}


//Higgs CS takes process ID, higgs mass mH, and COM energy sqrts in TeV (numbers are for 7 TeV only in this version)         
double HiggsCSandWidth::HiggsCSpdfErrMinus(int ID, double mH, double sqrts){

  /**********IDs*************/
  /*     ggToH = 1          */
  /*       VBF = 2          */
  /*        WH = 3          */
  /*        ZH = 4          */
  /*       ttH = 5          */
  /**************************/

  int i = 0;
  double closestMass = 0;
  double reqCSerr = 0;
  double tmpLow = 0, tmpHigh = 0;
  double deltaX = 0, deltaY = 0;
  double slope = 0;
  double step = 0;


  // If ID is unavailable return -1                           
  if(ID > ID_ttH || ID < ID_Total){return -1;}
  if(ID == ID_Total){return 0;}
  // If Ecm is not 7 TeV return -1                                                                 
  if(sqrts != 7){return -1;}
  //Don't interpolate btw 0 and numbers for mH300             
  if(ID > ID_VBF && mH > 300){return 0;}


  // If mH is out of range return -1                                                              
  // else find what array number to read                            
  if( mH < 90 || mH > 1000){return -1;}
  else{

    if(mH <= 110 ){step = 5; i = (int)((mH - 90)/step); closestMass = (int)(step*i + 90);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(4 + (mH - 110)/step); closestMass = (step*(i-4) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(64 + (mH - 140)/step); closestMass = (int)(step*(i-64) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(84 + (mH - 160)/step); closestMass = (int)(step*(i-84) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(149 + (mH - 290)/step); closestMass = (int)(step*(i-149) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(161 + (mH-350)/step); closestMass = (int)(step*(i-161) + 350);}
    if(mH > 400){step = 20; i = (int)(166 + (mH-400)/step); closestMass = (int)(step*(i-166) + 400);}



    tmpLow = CSpdfErrMinus[ID][i];
    tmpHigh = CSpdfErrMinus[ID][i+1];

    deltaX = mH - closestMass;


    deltaY = tmpHigh - tmpLow;
    slope = deltaY/step;

    // For partial widths                                                          
    if(deltaX == 0){ reqCSerr = tmpLow;}
    else{ reqCSerr = slope*deltaX + tmpLow;}
    reqCSerr *= .01; //Account for percentage                                                                                    
  }

  return reqCSerr;

}



// HiggsWidth takes process ID and higgs mass mH
double HiggsCSandWidth::HiggsWidth(int ID, double mH){


  /***********************IDs************************/
  /*                       Total = 0                */
  /*                       H->bb = 1                */
  /*                   H->tautau = 2                */
  /*                     H->mumu = 3                */
  /*                       H->ss = 4                */
  /*                       H->cc = 5                */
  /*                       H->tt = 6                */
  /*                       H->gg = 7                */
  /*                   H->gamgam = 8                */
  /*                     H->gamZ = 9                */
  /*                       H->WW = 10               */
  /*                       H->ZZ = 11               */
  /*                       H->4e = 12               */
  /*                    H->2e2mu = 13               */
  /*              H->4lep (e,mu) = 14               */
  /*          H->4lep (e,mu,tau) = 15               */
  /*                H->e+nu e-nu = 16               */
  /*               H->e+nu mu-nu = 17               */
  /*    H->2l2nu(l=e,mu)(nu=any) = 18               */
  /* H->2l2nu(l=e,mu,tau)(nu=any) = 19              */  
  /*    H->2l2q (l=e,mu)(q=udcsb) = 20              */
  /* H->2l2q(l=e,mu,tau)(q=udcsb) = 21              */
  /* H->l+nu qq(*) (l=e,mu)(q=udcsb) = 22           */
  /*  H->2nu2q (nu=any)(q=udcsb) = 23               */
  /*            H->4q (q=udcsb) = 24                */
  /*      H->4f (f=any fermion) = 25                */
  /**************************************************/



  double TotalWidth = 0;
  double PartialWidth = 0;
  double Width = 0;
  int i = 0;
  double closestMass = 0;
  double tmpLow1, tmpHigh1, deltaX, deltaY1, slope1;
  double deltaY2, tmpLow2, tmpHigh2, slope2, step;


  // If ID is unavailable return -1                                           
  if(ID > 25 || ID < 0){return -1;}


  // If mH is out of range return -1                                            
  // else find what array number to read                                        
  if( mH < 90 || mH > 1000){return -1;}
  else{

    //Find index and closest higgs mass for which we have numbers
    if(mH <=110 ){step = 5; i = (int)((mH - 90)/step); closestMass = (int)(step*i + 90);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(4 + (mH-110)/step); closestMass = (step*(i-4) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(64 + (mH-140)/step); closestMass = (int)(step*(i-64) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(84 + (mH-160)/step); closestMass = (int)(step*(i-84) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(149 + (mH-290)/step); closestMass = (int)(step*(i-149) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(161 + (mH-350)/step); closestMass = (int)(step*(i-161) + 350);}
    if(mH > 400 && mH <= 600 ){step = 20; i = (int)(166 + (mH-400)/step); closestMass = (int)(step*(i-166) + 400);}
    if(mH > 600){step = 10; i = (int)(176 + (mH-600)/step); closestMass = (int)(step*(i-176) + 600);}


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
