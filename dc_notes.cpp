// Cp utils
#include "cp_util/dc_constants.hpp"
#include "cp_util/dc_classes.hpp"
#include "cp_util/dc_funcs.hpp"
#include "include/cpprint.hpp"
using namespace cpprint;
#define print(...) do { constexpr int w=80; std::string l(w,'='); std::cout<<"Line "<<__LINE__<<" : "<<#__VA_ARGS__<<"\n"<<l<<"\n"; pprint(__VA_ARGS__); std::cout<<l<<"\n"; } while(0);
#define printi(...) do { constexpr int w=80; std::string l(w,'='); std::cout<<"Line "<<__LINE__<<" : "<<#__VA_ARGS__<<"\n"<<l<<"\n"; pprint_inline(__VA_ARGS__); std::cout<<"\n"<<l<<"\n"; } while(0);


template<typename... Args>
void variadic_print(const Args &... args) { ((std::cout << generate_container_string_recursively(args) << "\n"), ...); }

#include <bits/stdc++.h>
using namespace std;
// ********************** Modify Code Below ***********************************************************************

int main () {

    // ********************************** Usage of cp_utils ********************************************

    // dc_constants
    print(DIR);

    // dc_classes
    ufds uf(5);
    uf.unionSets(2,1);
    print(uf.find(2)==uf.find(1));

    // dc_funcs
    vector<int> vec = {1,2,3};
    print(permutations(vec));
    print(combinations(vec));
    // ********************************** Useful Syntax/ Tricks ********************************************

    // Flatten 2d vector to 1d -> use formula i*n+j for access
    int m = 5, n = 6, i = 2, j = 3;
    vector<int> dp1d(m * n, -INFINITY);
    print(dp1d[i*n+j]);
    // this removes the need for dp2d below
    vector<vector<int> > dp2d(m, vector<int>(n, -INFINITY));

    // useful syntax for recursive lambdas - fib
    auto recurse = [&](this auto func, int n) -> int {
        if (n == 1) { return 0; }
        if (n == 2) { return 1; }
        return func(n - 1) + func(n - 2);
    };
    print(recurse(5));

    return 0;
}