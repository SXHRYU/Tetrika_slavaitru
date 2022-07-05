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
