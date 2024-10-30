a_list = [1,2,3,4,5]

i=0
print(a_list[:i])
print(a_list[i+1:])

a_list.append(10)
a_list.append(11)
print(a_list)


class Solution:
    
    def get_difference_array(self, nums):
        
        diff_array = []
        
        for i in range(len(nums)):
            
            left_sum = sum(nums[:i])
            if i != len(nums) - 1:
                right_sum = sum(nums[i+1:])
            else:
                right_sum = 0
            
            diff_array.append(abs(left_sum - right_sum))
            print(diff_array)

soln = Solution()
nums = [1,2,3,4,5]
soln.get_difference_array(nums)