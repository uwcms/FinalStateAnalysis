#include <iostream>
float MuIso(float pt, float eta, float run) {
   if (run < 2) {
      if (pt >= 0 && pt < 8) {
         return 1.0;
      }
      if (pt >= 8 && pt < 10) {
         if (eta >= 0 && eta < 1.44) {
            return 0.968;
         }
         if (eta >= 1.44) {
            return 0.936;
         }
      }
      if (pt >= 10 && pt < 20) {
         if (eta >= 0 && eta < 1.44) {
            return 0.992;
         }
         if (eta >= 1.44) {
            return 0.99;
         }
      }
      if (pt >= 20 && pt < 30) {
         if (eta >= 0 && eta < 1.44) {
            return 1.0;
         }
         if (eta >= 1.44) {
            return 0.998;
         }
      }
      if (pt >= 30 && pt < 50) {
         if (eta >= 0 && eta < 1.44) {
            return 1.0;
         }
         if (eta >= 1.44) {
            return 0.998;
         }
      }
      if (pt >= 50 && pt < 100) {
         if (eta >= 0 && eta < 1.44) {
            return 1.0;
         }
         if (eta >= 1.44) {
            return 1.0;
         }
      }
      if (pt >= 100) {
         if (eta >= 0 && eta < 1.44) {
            return 1.0;
         }
         if (eta >= 1.44) {
            return 1.0;
         }
      }
   }
   if (run >= 2) {
      return 1.0;
   }
   std::cerr << "Warning out of bounds in function MuIso" << std::endl;
   return -999;
}

float MuHLT8(float pt, float eta, float run) {
   if (run < 2) {
      if (pt >= 0 && pt < 8) {
         return 1.0;
      }
      if (pt >= 8 && pt < 10) {
         if (eta >= 0 && eta < 1.44) {
            return 0.972;
         }
         if (eta >= 1.44) {
            return 1.003;
         }
      }
      if (pt >= 10 && pt < 20) {
         if (eta >= 0 && eta < 1.44) {
            return 0.989;
         }
         if (eta >= 1.44) {
            return 0.988;
         }
      }
      if (pt >= 20 && pt < 30) {
         if (eta >= 0 && eta < 1.44) {
            return 0.987;
         }
         if (eta >= 1.44) {
            return 0.987;
         }
      }
      if (pt >= 30 && pt < 50) {
         if (eta >= 0 && eta < 1.44) {
            return 0.986;
         }
         if (eta >= 1.44) {
            return 0.984;
         }
      }
      if (pt >= 50 && pt < 100) {
         if (eta >= 0 && eta < 1.44) {
            return 0.985;
         }
         if (eta >= 1.44) {
            return 0.982;
         }
      }
      if (pt >= 100) {
         if (eta >= 0 && eta < 1.44) {
            return 0.982;
         }
         if (eta >= 1.44) {
            return 0.982;
         }
      }
   }
   if (run >= 2) {
      return 1.0;
   }
   std::cerr << "Warning out of bounds in function MuHLT8" << std::endl;
   return -999;
}

float MuID(float pt, float eta, float run) {
   if (run < 2) {
      if (pt >= 0 && pt < 8) {
         return 1.0;
      }
      if (pt >= 8 && pt < 10) {
         if (eta >= 0 && eta < 1.44) {
            return 1.005;
         }
         if (eta >= 1.44) {
            return 0.955;
         }
      }
      if (pt >= 10 && pt < 20) {
         if (eta >= 0 && eta < 1.44) {
            return 0.986;
         }
         if (eta >= 1.44) {
            return 0.979;
         }
      }
      if (pt >= 20 && pt < 30) {
         if (eta >= 0 && eta < 1.44) {
            return 0.989;
         }
         if (eta >= 1.44) {
            return 0.976;
         }
      }
      if (pt >= 30 && pt < 50) {
         if (eta >= 0 && eta < 1.44) {
            return 0.991;
         }
         if (eta >= 1.44) {
            return 0.975;
         }
      }
      if (pt >= 50 && pt < 100) {
         if (eta >= 0 && eta < 1.44) {
            return 0.99;
         }
         if (eta >= 1.44) {
            return 0.978;
         }
      }
      if (pt >= 100) {
         if (eta >= 0 && eta < 1.44) {
            return 0.99;
         }
         if (eta >= 1.44) {
            return 0.978;
         }
      }
   }
   if (run >= 2) {
      return 1.0;
   }
   std::cerr << "Warning out of bounds in function MuID" << std::endl;
   return -999;
}

