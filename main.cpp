// Cp utils
#include "cp_util/dc_constants.hpp"
#include "cp_util/dc_classes.hpp"
#include "cp_util/dc_funcs.hpp"
#include "include/cpprint.hpp"
using namespace cpprint;
#define print(...) \
do { \
    constexpr int width = 80; \
    std::string line(width, '='); \
    std::cout << "Line " << __LINE__ << " : " << #__VA_ARGS__ << "\n" << line << "\n"; \
    variadic_print(__VA_ARGS__); \
    std::cout << line << "\n"; \
} while(0);

template<typename... Args>
void variadic_print(const Args &... args) { ((std::cout << generate_container_string_recursively(args) << "\n"), ...); }

#include <bits/stdc++.h>
using namespace std;
// ********************** Modify Code Below ***********************************************************************

class Solution {
public:
    vector<int> twoSum(vector<int> &nums, int target) {
        unordered_map<int, int> seen; // number -> index
        for (int i = 0; i < nums.size(); ++i) {
            int complement = target - nums[i];
            if (seen.count(complement)) {
                return {seen[complement], i};
            }
            seen[nums[i]] = i;
        }
        return {}; // just in case no solution is found
    }
};

int main() {
    vector<int> nums = {1, 2, 3, 10};
    int target = 11;

    Solution s;
    // Demo
    // 1) Add print statements for seen, and for nums
    // 2) showcase 2 forge
    // 3) showcase debug mode
    vector<vector<int> > dp(5, vector<int>(6, -1));
    print("ab", "cd", dp)
    print("ab", "cd", dp)
}
