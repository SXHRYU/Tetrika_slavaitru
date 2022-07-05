from TEST import check_answer

######### 1 task #########
tests = [
    {
    "input": [1],
    "output": "No zeroes"
    },
    {
    "input": [0],
    "output": 0
    },
    {
    "input": [1,0],
    "output": 1
    },
    {
    "input": [1,1,1,1,1],
    "output": "No zeroes"
    },
    {
    "input": [1,1,1,1,0,0,0,0],
    "output": 4
    },
    {
    "input": [1,0,0,0,0],
    "output": 1
    },
    {
    "input": [0,0,0,0,0],
    "output": 0
    },
    {
    "input": [],
    "output": "No zeroes"
    },
    {
    "input": [0],
    "output": 0
    },
]

# Solution assumes 0-indexed array which returns 1'st index of 0,
# else returns message.

def search_0(array: list[int]) -> int:
    if not array:
        return "No zeroes"
    else:
        left = 0
        right = len(array) - 1
        while left <= right:
            mid = (left + right) // 2
            if array[mid] == 1:
                left = mid + 1
            elif array[mid] == 0 and array[mid-1] == 0 and mid-1 != -1:
                right = mid - 1
            elif array[mid] == 0:
                return mid
        return "No zeroes"

check_answer(tests, search_0)
