#include "FinalStateAnalysis/PatTools/interface/PFMEtSignInterfaceBase.h"

#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "RecoMET/METAlgorithms/interface/significanceAlgo.h"

#include <TMath.h>
#include <TVectorD.h>

const double defaultPFMEtResolutionX = 10.;
const double defaultPFMEtResolutionY = 10.;

const double epsilon = 1.e-9;

PFMEtSignInterfaceBase::PFMEtSignInterfaceBase(const edm::ParameterSet& cfg)
  : pfMEtResolution_(0)
{
  pfMEtResolution_ = new metsig::SignAlgoResolutions(cfg);

  verbosity_ = cfg.exists("verbosity") ?
    cfg.getParameter<int>("verbosity") : 0;
}

PFMEtSignInterfaceBase::~PFMEtSignInterfaceBase()
{
  delete pfMEtResolution_;
}

TMatrixD PFMEtSignInterfaceBase::convert_matrix(const ROOT::Math::SMatrix2D& mat) const
{
  TMatrixD output = TMatrixD(mat.kRows, mat.kCols, mat.Array());
  return output;
}

TMatrixD PFMEtSignInterfaceBase::convert_matrix(const TMatrixD& mat) const
{
  return mat;
}

TMatrixD PFMEtSignInterfaceBase::operator()(const std::list<const reco::Candidate*>& particles) const
{
  if ( this->verbosity_ ) {
    std::cout << "<PFMEtSignInterfaceBase::operator()>:" << std::endl;
    std::cout << " particles: entries = " << particles.size() << std::endl;
  }

  std::vector<metsig::SigInputObj> pfMEtSignObjects;
  addPFMEtSignObjects(pfMEtSignObjects, particles);

  return this->operator()(pfMEtSignObjects);
}

TMatrixD PFMEtSignInterfaceBase::operator()(const std::vector<metsig::SigInputObj>& pfMEtSignObjects) const
{
  if ( this->verbosity_ ) {
    std::cout << "<PFMEtSignInterfaceBase::operator()>:" << std::endl;
    std::cout << " pfMEtSignObjects: entries = " << pfMEtSignObjects.size() << std::endl;
    double dpt2Sum = 0.;
    for ( std::vector<metsig::SigInputObj>::const_iterator pfMEtSignObject = pfMEtSignObjects.begin();
	  pfMEtSignObject != pfMEtSignObjects.end(); ++pfMEtSignObject ) {
      std::cout
        //<< pfMEtSignObject->get_type()
        << ": pt = " << pfMEtSignObject->get_energy() << ","
		<< " phi = " << pfMEtSignObject->get_phi() << " --> dpt = " << pfMEtSignObject->get_sigma_e() << std::endl;
      dpt2Sum += pfMEtSignObject->get_sigma_e();
    }
    std::cout << "--> sqrt(sum(dpt^2)) = " << TMath::Sqrt(dpt2Sum) << std::endl;
  }

  TMatrixD pfMEtCov(2,2);
  if ( pfMEtSignObjects.size() >= 2 ) {
    metsig::significanceAlgo pfMEtSignAlgorithm;
    pfMEtSignAlgorithm.addObjects(pfMEtSignObjects);
    pfMEtCov = convert_matrix(pfMEtSignAlgorithm.getSignifMatrix());

    if ( this->verbosity_ && TMath::Abs(pfMEtCov.Determinant()) > epsilon ) {
      TVectorD eigenValues(2);
      TMatrixD eigenVectors = pfMEtCov.EigenVectors(eigenValues);
      // CV: eigenvectors are stored in columns
      //     and are sorted such that the one corresponding to the highest eigenvalue is in the **first** column
      for ( unsigned iEigenVector = 0; iEigenVector < 2; ++iEigenVector ) {
	std::cout << "eigenVector #" << iEigenVector << " (eigenValue = " << eigenValues(iEigenVector) << "):"
		  << " x = " << eigenVectors(0, iEigenVector) << ", y = " << eigenVectors(1, iEigenVector) << std::endl;
      }
    }

//--- substitute (PF)MEt resolution matrix by default values
//    in case resolution matrix cannot be inverted
    if ( TMath::Abs(pfMEtCov.Determinant()) < epsilon ) {
      edm::LogWarning("PFMEtSignInterfaceBase::operator()")
	<< "Inversion of PFMEt covariance matrix failed, det = " << pfMEtCov.Determinant()
	<< " --> replacing covariance matrix by resolution defaults !!";
      pfMEtCov(0,0) = (defaultPFMEtResolutionX*defaultPFMEtResolutionX);
      pfMEtCov(0,1) = 0.;
      pfMEtCov(1,0) = 0.;
      pfMEtCov(1,1) = (defaultPFMEtResolutionY*defaultPFMEtResolutionY);
    }
  } else {
    pfMEtCov(0,0) = 0.;
    pfMEtCov(0,1) = 0.;
    pfMEtCov(1,0) = 0.;
    pfMEtCov(1,1) = 0.;
  }

  return pfMEtCov;
}

