'''
LeetCode Problem 1: Two Sum
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
You may assume that each input would have exactly one solution, and you may not use the same element twice.
'''
def twoSum(nums, target):
      hash_map = {}
      for i, num in enumerate(nums):
          difference = target - num
          if difference in hash_map:
            return [hash_map[difference], i]
          hash_map[num] = i
      return []