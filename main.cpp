// Cp utils
#include "cp_util/dc_constants.hpp"
#include "cp_util/dc_classes.hpp"
#include "cp_util/dc_funcs.hpp"
#include "include/cpprint.hpp"
using namespace cpprint;
#define print(x) \
do { \
constexpr int width = 80; \
std::string line(width, '='); \
std::cout << "Line " << __LINE__ << " : " << #x << "\n" << line << "\n"; \
pprint(x); \
std::cout << line << "\n"; \
} while(0);

#include <bits/stdc++.h>
using namespace std;
// ********************** Modify Code Below ***********************************************************************

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
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

int main(){
    vector<int> nums = {1,2,3,10};
    int target = 11;

    Solution s;
    // Demo
    // 1) Add print statements for seen, and for nums
    // 2) showcase 2 forge
    // 3) showcase debug mode
    print(s.twoSum(nums,11));

}