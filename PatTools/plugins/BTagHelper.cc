// b tag systematics related
#include "TRandom3.h"


bool applySF(bool& isBTagged, float Btag_SF, float Btag_eff){
    TRandom3 * rand_;
    rand_ = new TRandom3(0);
    //rand_ = new TRandom3(12345);

    bool newBTag = isBTagged;

    if (Btag_SF == 1) return newBTag; //no correction needed 

    //throw die
    float coin = rand_->Uniform();    
    //std::cout<<"Uniform coin: "<<coin<<std::endl;

    if(Btag_SF > 1){  // use this if SF>1

        if( !isBTagged ) {

            //fraction of jets that need to be upgraded
            float mistagPercent = (1.0 - Btag_SF) / (1.0 - (Btag_SF/Btag_eff) );

            //upgrade to tagged
            if( coin < mistagPercent ) {newBTag = true;}
        }

    }else{  // use this if SF<1

        //downgrade tagged to untagged
        if( isBTagged && coin > Btag_SF ) {newBTag = false;}

    }

    return newBTag;
}
