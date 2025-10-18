// Cp utils
#include "cp_util/dc_constants.hpp"
#include "cp_util/dc_classes.hpp"
#include "cp_util/dc_funcs.hpp"
#include "include/cpprint.hpp"
using namespace cpprint;
#define print(x) \
do { \
std::cout << "Line " << __LINE__ << " : " << #x << " =============================================================\n"; \
pprint(x); \
std::cout << "=====================================================================================================\n"; \
} while(0)

#include <bits/stdc++.h>
using namespace std;
// ********************** Modify Code Below ***********************************************************************

int main(){
 print("hello");
}