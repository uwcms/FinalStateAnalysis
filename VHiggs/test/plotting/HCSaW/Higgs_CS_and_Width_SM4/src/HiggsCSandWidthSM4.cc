#ifndef HIGGSCSANDWIDTHSM4_CC
#define HIGGSCSANDWIDTHSM4_CC


#include <iostream>
#include <cmath>
#include <string>
#include <cstdlib>
#include <fstream>

#include "HiggsCSandWidthSM4.h"

using namespace std;

HiggsCSandWidthSM4::HiggsCSandWidthSM4()
{


  ifstream file;
 
  // Read Widths into memory
  FileLoc = "../txtFiles/Higgs_BR_SM4.txt"; //directory of input file
  const char* BranchRatioFileLoc = FileLoc.c_str(); 
  file.open(BranchRatioFileLoc);
  for(int k = 0; k < 102; k++){

    file >> scratchMass >> BR[0][k] >> BR[1][k] >> BR[2][k] >> BR[3][k] >> BR[4][k] >> BR[5][k] >> BR[6][k] >> BR[7][k] >> BR[8][k] >> BR[9][k]
	 >> BR[10][k] >> BR[11][k] >> BR[12][k] >> BR[13][k] >> BR[14][k] >> BR[15][k] >> BR[16][k] >> BR[17][k];


  }
  file.close();

  // Read CS into memory
  file.open("../txtFiles/HiggsCS_Official_SM4.txt");//directory of input file
  for(int k = 0; k < 109; k++){

    file >> scratchMass >> CS[ID_ggToH][k];// >> CS[ID_VBF][k] >> CS[ID_WH][k] >> CS[ID_ZH][k] >> CS[ID_ttH][k] >> CS[ID_Total][k];

    // cout << scratchMass << "  " << CS[ID_ggToH][k] << endl;

  }
  file.close();

  file.open("../txtFiles/HiggsCS_Error_Official_SM4.txt");//directory of input file                       
  for(int k = 0; k < 175; k++){

    file >> scratchMass >> CSerrPlus[ID_ggToH][k] >> CSerrMinus[ID_ggToH][k] >> CSscaleErrPlus[ID_ggToH][k] >> CSscaleErrMinus[ID_ggToH][k]
	 >> CSpdfErrPlus[ID_ggToH][k] >> CSpdfErrMinus[ID_ggToH][k];

  }
  file.close();


}


HiggsCSandWidthSM4::~HiggsCSandWidthSM4()
{
  //destructor

}


//Higgs CS takes process ID, higgs mass mH, and COM energy sqrts in TeV (numbers are for 7 TeV only in this version)
double HiggsCSandWidthSM4::HiggsCS(int ID, double mH, double sqrts){

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
  if(ID > ID_ggToH || ID < ID_ggToH){return 0;}
  // If Ecm is not 7 TeV return -1
  if(sqrts != 7){return -1;}
 

  // If mH is out of range return -1                                           
  // else find what array number to read         
  if( mH < 100 || mH > 1000){return 0;}
  else{


    //Find index and closest higgs mass for which we have numbers
    if(mH <= 140){step = 10; i = (int)((mH - 100)/step); closestMass = (int)(step*i + 100);}
    if(mH > 140 && mH <= 150 ){step = 5; i = (int)(4 + (mH-140)/step); closestMass = (step*(i-4) + 140);}
    if(mH > 150 && mH <= 190 ){step = 1; i = (int)(6 + (mH-150)/step); closestMass = (int)(step*(i-6) + 150);}
    if(mH > 190 && mH <= 200 ){step = 5; i = (int)(46 + (mH-190)/step); closestMass = (int)(step*(i-46) + 190);}
    if(mH > 200 && mH <= 330 ){step = 10; i = (int)(48 + (mH-200)/step); closestMass = (int)(step*(i-48) + 200);}
    if(mH > 330 && mH <= 335 ){step = 5; i = (int)(61 + (mH-330)/step); closestMass = (int)(step*(i-61) + 330);}
    if(mH > 335 && mH <= 355 ){step = 1; i = (int)(62 + (mH-335)/step); closestMass = (int)(step*(i-62) + 335);}
    if(mH > 355 && mH <= 360 ){step = 5; i = (int)(82 + (mH-355)/step); closestMass = (int)(step*(i-82) + 355);}
    if(mH > 360 && mH <= 370 ){step = 10; i = (int)(83 + (mH-360)/step); closestMass = (int)(step*(i-83) + 360);}
    if(mH > 370 && mH <= 380 ){step = 5; i = (int)(84 + (mH-370)/step); closestMass = (int)(step*(i-84) + 370);}
    if(mH > 380 && mH <= 500 ){step = 10; i = (int)(86 + (mH-380)/step); closestMass = (int)(step*(i-86) + 380);}
    if(mH > 500 && mH <= 1000 ){step = 50; i = (int)(98 + (mH-500)/step); closestMass = (int)(step*(i-98) + 500);}


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
double HiggsCSandWidthSM4::HiggsCSErrPlus(int ID, double mH, double sqrts){

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
  if(ID > ID_ggToH || ID < ID_ggToH){return 0;}
  // If Ecm is not 7 TeV return -1                                                                                                
  if(sqrts != 7){return -1;}
 
  // If mH is out of range return -1                                                                        
  // else find what array number to read                                          
  if( mH < 100 || mH > 600){return 0;}
  else{

    if(mH <= 110 ){step = 5; i = (int)((mH - 100)/step); closestMass = (int)(step*i + 100);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(2 + (mH - 110)/step); closestMass = (step*(i-2) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(62 + (mH - 140)/step); closestMass = (int)(step*(i-62) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(82 + (mH - 160)/step); closestMass = (int)(step*(i-82) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(147 + (mH - 290)/step); closestMass = (int)(step*(i-147) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(159 + (mH-350)/step); closestMass = (int)(step*(i-159) + 350);}
    if(mH > 400){step = 20; i = (int)(164 + (mH-400)/step); closestMass = (int)(step*(i-164) + 400);}




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
double HiggsCSandWidthSM4::HiggsCSErrMinus(int ID, double mH, double sqrts){

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
  if(ID > ID_ggToH || ID < ID_ggToH){return 0;}

  // If Ecm is not 7 TeV return -1                                                                                           
  if(sqrts != 7){return -1;}
  
  // If mH is out of range return -1                                                                           
  // else find what array number to read                                                                 
  if( mH < 100 || mH > 600){return 0;}
  else{

    if(mH <= 110 ){step = 5; i = (int)((mH - 100)/step); closestMass = (int)(step*i + 100);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(2 + (mH - 110)/step); closestMass = (step*(i-2) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(62 + (mH - 140)/step); closestMass = (int)(step*(i-62) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(82 + (mH - 160)/step); closestMass = (int)(step*(i-82) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(147 + (mH - 290)/step); closestMass = (int)(step*(i-147) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(159 + (mH-350)/step); closestMass = (int)(step*(i-159) + 350);}
    if(mH > 400){step = 20; i = (int)(164 + (mH-400)/step); closestMass = (int)(step*(i-164) + 400);}




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
double HiggsCSandWidthSM4::HiggsCSscaleErrPlus(int ID, double mH, double sqrts){

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
  if(ID > ID_ggToH || ID < ID_ggToH){return 0;}

  // If Ecm is not 7 TeV return -1                                                
  if(sqrts != 7){return -1;}

  // If mH is out of range return -1                                                         
  // else find what array number to read                                                      
  if( mH < 100 || mH > 600){return 0;}
  else{

    if(mH <= 110 ){step = 5; i = (int)((mH - 100)/step); closestMass = (int)(step*i + 100);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(2 + (mH - 110)/step); closestMass = (step*(i-2) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(62 + (mH - 140)/step); closestMass = (int)(step*(i-62) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(82 + (mH - 160)/step); closestMass = (int)(step*(i-82) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(147 + (mH - 290)/step); closestMass = (int)(step*(i-147) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(159 + (mH-350)/step); closestMass = (int)(step*(i-159) + 350);}
    if(mH > 400){step = 20; i = (int)(164 + (mH-400)/step); closestMass = (int)(step*(i-164) + 400);}




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
double HiggsCSandWidthSM4::HiggsCSscaleErrMinus(int ID, double mH, double sqrts){

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
  if(ID > ID_ggToH || ID < ID_ggToH){return 0;}

  // If Ecm is not 7 TeV return -1                                                               
  if(sqrts != 7){return -1;}
 
  // If mH is out of range return -1                        
  // else find what array number to read                              
  if( mH < 100 || mH > 600){return 0;}
  else{

    if(mH <= 110 ){step = 5; i = (int)((mH - 100)/step); closestMass = (int)(step*i + 100);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(2 + (mH - 110)/step); closestMass = (step*(i-2) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(62 + (mH - 140)/step); closestMass = (int)(step*(i-62) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(82 + (mH - 160)/step); closestMass = (int)(step*(i-82) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(147 + (mH - 290)/step); closestMass = (int)(step*(i-147) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(159 + (mH-350)/step); closestMass = (int)(step*(i-159) + 350);}
    if(mH > 400){step = 20; i = (int)(164 + (mH-400)/step); closestMass = (int)(step*(i-164) + 400);}



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
double HiggsCSandWidthSM4::HiggsCSpdfErrPlus(int ID, double mH, double sqrts){

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
  if(ID > ID_ggToH || ID < ID_ggToH){return 0;}

  // If Ecm is not 7 TeV return -1                                                                                         
  if(sqrts != 7){return -1;}
 


  // If mH is out of range return -1                                                                                  
  // else find what array number to read                                                              
  if( mH < 100 || mH > 600){return 0;}
  else{

    if(mH <= 110 ){step = 5; i = (int)((mH - 100)/step); closestMass = (int)(step*i + 100);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(2 + (mH - 110)/step); closestMass = (step*(i-2) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(62 + (mH - 140)/step); closestMass = (int)(step*(i-62) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(82 + (mH - 160)/step); closestMass = (int)(step*(i-82) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(147 + (mH - 290)/step); closestMass = (int)(step*(i-147) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(159 + (mH-350)/step); closestMass = (int)(step*(i-159) + 350);}
    if(mH > 400){step = 20; i = (int)(164 + (mH-400)/step); closestMass = (int)(step*(i-164) + 400);}




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
double HiggsCSandWidthSM4::HiggsCSpdfErrMinus(int ID, double mH, double sqrts){

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
  if(ID > ID_ggToH || ID < ID_ggToH){return 0;}

  // If Ecm is not 7 TeV return -1                                                                 
  if(sqrts != 7){return -1;}
  
  // If mH is out of range return -1                                                              
  // else find what array number to read                            
  if( mH < 100 || mH > 1000){return 0;}
  else{


    //Find index and closest higgs mass for which we have numbers
    if(mH <= 110 ){step = 5; i = (int)((mH - 100)/step); closestMass = (int)(step*i + 100);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(2 + (mH - 110)/step); closestMass = (step*(i-2) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(62 + (mH - 140)/step); closestMass = (int)(step*(i-62) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(82 + (mH - 160)/step); closestMass = (int)(step*(i-82) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(147 + (mH - 290)/step); closestMass = (int)(step*(i-147) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(159 + (mH-350)/step); closestMass = (int)(step*(i-159) + 350);}
    if(mH > 400){step = 20; i = (int)(164 + (mH-400)/step); closestMass = (int)(step*(i-164) + 400);}




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
double HiggsCSandWidthSM4::HiggsWidth(int ID, double mH){


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
  /*                   H->4e/4mu = 12               */
  /*                    H->2e2mu = 13               */
  /*             H->4l(e/mu/tau) = 14               */
  /*                       H->4q = 15               */
  /*                     H->2l2q = 16               */
  /*                       H->4f = 17               */
  /**************************************************/



  double TotalWidth = 0;
  double PartialWidth = 0;
  double Width = 0;
  int i = 0;
  double closestMass = 0;
  double tmpLow1, tmpHigh1, deltaX, deltaY1, slope1;
  double deltaY2, tmpLow2, tmpHigh2, slope2, step;


  // If ID is unavailable return -1                                           
  if(ID > 17 || ID < 0){return 0;}


  // If mH is out of range return -1                                            
  // else find what array number to read                                        
  if( mH < 100 || mH > 1000){return 0;}
  else{

    //Find index and closest higgs mass for which we have numbers
    if(mH <= 140){step = 10; i = (int)((mH - 100)/step); closestMass = (int)(step*i + 100);}
    if(mH > 140 && mH <= 150 ){step = 5; i = (int)(4 + (mH-140)/step); closestMass = (step*(i-4) + 140);}
    if(mH > 150 && mH <= 190 ){step = 1; i = (int)(6 + (mH-150)/step); closestMass = (int)(step*(i-6) + 150);}
    if(mH > 190 && mH <= 200 ){step = 5; i = (int)(46 + (mH-190)/step); closestMass = (int)(step*(i-46) + 190);}
    if(mH > 200 && mH <= 330 ){step = 10; i = (int)(48 + (mH-200)/step); closestMass = (int)(step*(i-48) + 200);}
    if(mH > 330 && mH <= 335 ){step = 5; i = (int)(61 + (mH-330)/step); closestMass = (int)(step*(i-61) + 330);}
    if(mH > 335 && mH <= 340 ){step = 1; i = (int)(62 + (mH-335)/step); closestMass = (int)(step*(i-62) + 335);}
    if(mH > 340 && mH <= 345 ){step = 5; i = (int)(67 + (mH-340)/step); closestMass = (int)(step*(i-67) + 340);}
    if(mH > 345 && mH <= 355 ){step = 1; i = (int)(68 + (mH-345)/step); closestMass = (int)(step*(i-68) + 345);}
    if(mH > 355 && mH <= 360 ){step = 5; i = (int)(78 + (mH-355)/step); closestMass = (int)(step*(i-78) + 355);}
    if(mH > 360 && mH <= 370 ){step = 10; i = (int)(79 + (mH-360)/step); closestMass = (int)(step*(i-79) + 360);}
    if(mH > 370 && mH <= 380 ){step = 5; i = (int)(80 + (mH-370)/step); closestMass = (int)(step*(i-80) + 370);}
    if(mH > 380 && mH <= 500 ){step = 10; i = (int)(82 + (mH-380)/step); closestMass = (int)(step*(i-82) + 380);}
    if(mH > 500 && mH <= 800 ){step = 50; i = (int)(94 + (mH-500)/step); closestMass = (int)(step*(i-94) + 500);}
    if(mH > 800 && mH <= 1000 ){step = 200; i = (int)(100 + (mH-800)/step); closestMass = (int)(step*(i-100) + 800);}



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
