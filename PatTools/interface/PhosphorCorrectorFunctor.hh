#ifndef PHOSPHOR_CORRECTOR_FUNCTOR_HH
#define PHOSPHOR_CORRECTOR_FUNCTOR_HH 1

#include <string>
#include <utility>
#include <vector>
#include <map>
#include <fstream>
#include <math.h>
#include "TObject.h"
#include "TRandom3.h"

namespace zgamma{  
  using std::map;
  using std::string;
  
  class PhosphorCorrectionFunctor: public TObject{
    
  public:
    PhosphorCorrectionFunctor();
    PhosphorCorrectionFunctor(const char* filename);
    PhosphorCorrectionFunctor(const char* filename, bool R9Cat);//Bool just used to overload constructor and allow R9 categories inplementation
    ~PhosphorCorrectionFunctor();
    //~PhosphorCorrectionFunctor(){};//do nothing
    
    //Gets the corrected energy for photons in DATA 
    //double GetDataCorrection(double Pt, double Eta, int ringNumber);
    //Scale and
    //double GetMcCorrection(double Pt, double Eta, double genEnergy);

    double GetScaleCorr(int year, double pt, double eta);
    
    double FabSmear(double E, double eta, double r9);//Fabrice gaussian smearing (returns smeared Energy)
    
    double GetCorrEnergyMC(int year, double pt, double etaReco, double Egen);//returns corrected and smeared Energy for MC
    double GetCorrEnergyData(int year, double pt, double etaReco);//Overloading method for data->returns corrected data energy
    double GetCorrEnergyMC(float R9, int year, double pt, double etaReco, double Egen);//returns corrected and smeared Energy for MC and R9 Categories
    double GetCorrEnergyData(float R9, int year, double pt, double etaReco);//Overloading method for data->returns corrected data energy and R9 Categories

    //double GetCorrEnergy(int year, double pt, double etaReco, int datType);//Overloading method for data->returns corrected data energy

    double GetCorrEtMC(int year, double pt, double etaReco, double Egen);//returns corrected and smeared Et for MC
    double GetCorrEtData(int year, double pt, double etaReco);//Overloading method for data->returns corrected data Et
    
    double GetCorrEtMC(float R9, int year, double pt, double etaReco, double Egen);//returns corrected and smeared Et for MC and R9 Categories
    double GetCorrEtData(float R9, int year, double pt, double etaReco);//Overloading method for data->returns corrected data Et and R9 Categories

    //double GetCorrEt(int year, double pt, double etaReco, int datType);//Overloading method for data->returns corrected data Et

    //pair <int,double> ScaleEnError(float R9, int year, double pt, double etaReco, double Egen);
    //pair <int,double> ResEnError(float R9, int year, double pt, double etaReco, double Egen);

    double ScaleEnError(float R9, int year, double pt, double etaReco, double Egen);
    double ResEnError(float R9, int year, double pt, double etaReco, double Egen);
    
    int GetCategory(float R9, int year, double pt, double etaReco);//Get Category index(large number format)

    int* CatIndex(float R9, int year, double pt, double etaReco);//Return category numbers
    int GetCatNumber(int index);

    inline double EtoET(double E, double eta){return (double)E/cosh(eta);};
    inline double ETtoE(double Et, double eta){return (double)Et*cosh(eta);};

  private:

    enum Keys {XX_XI = 0,
	       XX_XII,
	       MC = 0,
	       Data, 
               EB = 0, 
               EE, 
	       Scale = 0,
               Res,
	       Pt0 = 0,
	       Pt1,
	       Pt2,
	       Pt3
    };
    
    // string MapKey;//fotmat Year_DataType_DetType_CorrType_PtBin
    map < string, double > CorrMap;
    map < string, double > ErrMap;
    map < int, int > CatMap;
    std::ifstream MapFile;
    const char* filename;

    //Private Methods
    std::string CreateMapKey(int Year, int DataType, int DetType, int CorrType, int PtBin);// Creates key in inclusive R9 categories
    std::string CreateMapKey(int Year, int DataType, int DetType,int R9Cat, int CorrType, int PtBin);// Creates key including R9 categories

    TRandom3* rand;
    
    
    bool SetMapFileName(const char* filename);
    
    bool MapCat();
    bool CreateMap();
    bool CreateMap(bool R9Cat);//Bool just used to overload method and allow R9 categories inplementation
    
  };



}//End namespace zgamma

#endif
