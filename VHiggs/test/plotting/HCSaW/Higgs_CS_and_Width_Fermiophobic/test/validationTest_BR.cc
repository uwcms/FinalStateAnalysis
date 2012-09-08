#include <iostream>
#include <iomanip>
#include <fstream>
#include <string>

#include "HiggsCSandWidthFermi.cc"

using namespace std;

int main()
{

  ofstream fileOut;
  char* fileName_[25] = {"Hbb.txt","Htautau.txt","Hmumu.txt","Hss.txt","Hcc.txt","Htt.txt","Hgg.txt","Hgamgam.txt","HgammaZ.txt","HWW.txt","HZZ.txt",
			"HZZ4e.txt","HZZ2e2mu.txt","HZZ4lep(emu).txt","HZZ4lep(emutau).txt","HWW2e2nu.txt","HWWeNuMuNu.txt","HZZ2l2nu(emu).txt",
			 "HZZ2l2nu(emutau).txt","HZZ2l2q(emu).txt","HZZ2l2q(emutau).txt","HWWlnuqq(emu).txt","HZZ2nu2q.txt","H4q.txt","H4f.txt"};
  string channel[25] = {"H->bb","H->tautau","H->mumu","H->ss","H->cc","H->tt","H->gg","H->gamgam","H->gammaZ","H->WW","H->ZZ",
			 "H->ZZ->4e","H->ZZ->2e2mu","H->ZZ->4lep(emu)","H->ZZ->4lep(emutau)","H->WW->2e2nu","H->WW->eNuMuNu","H->ZZ->2l2nu(emu)",
			"H->ZZ->2l2nu(emutau)","H->ZZ->2l2q(emu)","H->ZZ->2l2q(emutau)","H->WW->lnuqq(emu)","H->ZZ->2nu2q","H->4q","H->4f"};

  HiggsCSandWidthFermi *myCSW = new HiggsCSandWidthFermi();

  for( int i = 0; i < 25; i++)
    {
      
      fileOut.open(fileName_[i]);
      fileOut << " mH     Width   TotalCS    BR(H->ZZ)     BR("+channel[i]+")  " << endl;

      double mH;
      double Width;
      double CS = 0;
      double BRHZZ;
      double BRChan;
      double sqrts = 7;

      for( double j = 110; j < 140; j += 0.5)
	{

	  mH = j;
	  Width = myCSW->HiggsWidth(0,mH);
	  //CS = myCSW->HiggsCS(0,mH,sqrts);
	  BRHZZ = myCSW->HiggsWidth(11,mH)/myCSW->HiggsWidth(0,mH);
	  BRChan = myCSW->HiggsWidth(i+1,mH)/myCSW->HiggsWidth(0,mH);
	 

	  fileOut << setw(6) << mH << " " << setw(6) << Width << "   " << setw(6) << CS << "   " << setw(6) << BRHZZ << "   " << setw(6) << BRChan << endl;

	}



      for( double k = 140; k < 160; k++ )
	{

          mH = k;
          Width = myCSW->HiggsWidth(0,mH);
          //CS = myCSW->HiggsCS(0,mH,sqrts);
          BRHZZ = myCSW->HiggsWidth(11,mH)/myCSW->HiggsWidth(0,mH);
          BRChan = myCSW->HiggsWidth(i+1,mH)/myCSW->HiggsWidth(0,mH);


          fileOut << setw(6) << mH << " " << setw(6) << Width << "   " << setw(6) << CS << "   " << setw(6) << BRHZZ << "   " << setw(6) << BRChan << endl;



	}

      for( double l = 160; l < 290; l += 2)
	{
          mH = l;
          Width = myCSW->HiggsWidth(0,mH);
          //CS = myCSW->HiggsCS(0,mH,sqrts);
          BRHZZ = myCSW->HiggsWidth(11,mH)/myCSW->HiggsWidth(0,mH);
          BRChan = myCSW->HiggsWidth(i+1,mH)/myCSW->HiggsWidth(0,mH);


          fileOut << setw(6) << mH << " " << setw(6) << Width << "   " << setw(6) << CS << "   " << setw(6) << BRHZZ << "   " << setw(6) << BRChan << endl;


	}

      for( double m = 290; m < 350; m += 5)
	{

          mH = m;
          Width = myCSW->HiggsWidth(0,mH);
          //CS = myCSW->HiggsCS(0,mH,sqrts);
          BRHZZ = myCSW->HiggsWidth(11,mH)/myCSW->HiggsWidth(0,mH);
          BRChan = myCSW->HiggsWidth(i+1,mH)/myCSW->HiggsWidth(0,mH);


          fileOut << setw(6) << mH << " " << setw(6) << Width << " " << setw(6) << CS << " " << setw(6) << BRHZZ << " " << setw(6) << BRChan << endl;



	}

      for( double n = 350; n < 400; n += 10)
	{

          mH = n;
          Width = myCSW->HiggsWidth(0,mH);
          //CS = myCSW->HiggsCS(0,mH,sqrts);
          BRHZZ = myCSW->HiggsWidth(11,mH)/myCSW->HiggsWidth(0,mH);
          BRChan = myCSW->HiggsWidth(i+1,mH)/myCSW->HiggsWidth(0,mH);


          fileOut << setw(6) << mH << " " << setw(6) << Width << "   " << setw(6) << CS << "   " << setw(6) << BRHZZ << "   " << setw(6) << BRChan << endl;



	}

      for( double q = 400; q <= 1000; q += 20 )
	{

          mH = q;
          Width = myCSW->HiggsWidth(0,mH);
          //CS = myCSW->HiggsCS(0,mH,sqrts);
          BRHZZ = myCSW->HiggsWidth(11,mH)/myCSW->HiggsWidth(0,mH);
          BRChan = myCSW->HiggsWidth(i+1,mH)/myCSW->HiggsWidth(0,mH);


          fileOut << setw(6) << mH << " " << setw(6) << Width << "   " << setw(6) << CS << "   " << setw(6) << BRHZZ << "   " << setw(6) << BRChan << endl;


	}

      fileOut.close();

    }




  return 0;

}
