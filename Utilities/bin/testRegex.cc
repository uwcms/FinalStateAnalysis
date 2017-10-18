#include <boost/regex.hpp>
#include <iostream>
#include <string>

/*
 * Simple utility to test a boost::regex
 *
 * Author: Evan K. Friis, UW Madison
 */

int main(int argc, char* argv[])
{
  // only allow one argument for this simple example which should be the
  // the python cfg file
  if ( argc < 3 ) {
    std::cout << "Usage : " << argv[0] <<
      " [test_string] [test_regex]" << std::endl;
    return 1;
  }

  std::string test_string(argv[1]);
  std::string test_regex(argv[2]);

  boost::regex regexp(test_regex);

  bool match = boost::regex_match(test_string, regexp);

  std::cout << "Regex test result.  NB || only delimit the start and end." << std::endl;
  std::cout << "Test string: ||" << test_string << "||" << std::endl;
  std::cout << "Test regexp: ||" << test_regex << "||" << std::endl;
  std::cout << "Match: " << match << std::endl;

}
