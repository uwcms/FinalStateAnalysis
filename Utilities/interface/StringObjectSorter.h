#ifndef STRINGOBJECTSORTER_ZIL3S41B
#define STRINGOBJECTSORTER_ZIL3S41B

/*
 * StringObjectSorter
 *
 * Author: Evan K. Friis
 *
 * Class which implements a predicate to sort objects of a given type using
 * the StringObjectFunction.  Default order is descending.
 *
 */

#include <cassert>
#include <functional>
#include "CommonTools/Utils/interface/StringObjectFunction.h"

template<class T>
class StringObjectSorter : public std::binary_function<const T*, const T*, bool> {
  public:
    StringObjectSorter(const std::string& function, bool descending=true, bool lazy=true):
      function_(function, lazy),descending_(descending) {}
    bool operator()(const T* t1, const T* t2) const {
      assert(t1);
      assert(t2);
      //if (!t1 || !t2) {
        //std::cout << "WTF: " << t1 << " " << t2 << std::endl;
      //}
      //std::cout << "t1: " << t1 << " func " << function_(*t1) << std::endl;
      //std::cout << "t2: " << t2 << " func " << function_(*t2) << std::endl;
      bool lessThan = function_(*t1) < function_(*t2);
      // Descending inverts lessThan via xor if true
      if (descending_)
        return !lessThan;
      else
        return lessThan;
    }
  private:
    const StringObjectFunction<T> function_;
    bool descending_;
};

#endif /* end of include guard: STRINGOBJECTSORTER_ZIL3S41B */
