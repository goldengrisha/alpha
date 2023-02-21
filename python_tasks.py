"""
Write an application in any of the following languages (Scala/Python/Java) that adds a specific character before every occurrence of a character sequence in a string.
What is the complexity of your solution?
"""


def add_string_into_specific_position(word, target, injection):
    """
    regarding the code documentation, average case of O(N) and a worst case of O(N+M).
    """
    if word is None or len(word) == 0 or len(target) == 0:
        return word

    result = word.replace(target, f"{injection}{target}")
    return result


assert (
    add_string_into_specific_position("abcalphacdealphaxalph", "alpha", "_")
    == "abc_alphacde_alphaxalph"
)


"""
Write an application in any of the following languages (Scala/Java/Python):
Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].
The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.
You must write an algorithm that runs in O(n) time and without using the division operation.
"""


def all_products(arr):
    arr_len = len(arr)
    if arr is None or arr_len == 0 or arr_len == 1:
        return arr

    ans = [1] * arr_len
    for i in range(1, arr_len):
        ans[i] = arr[i - 1] * ans[i - 1]
        right = 1

    for i in range(arr_len - 1, -1, -1):
        ans[i] *= right
        right *= arr[i]

    return ans


assert all_products([2, 3, 5, 1]) == [15, 10, 6, 30]


"""
Write an application in any of the following languages (Scala/Java/Python):
Given an integer array A of size 10, with unordered numbers between 0-9, find out which number is missing
"""


def missed_number(arr):
    arr_len = len(arr)
    if arr is None or arr_len == 0 or arr_len == 1:
        return arr
    sorted_arr = sorted(arr)

    for i in range(1, arr_len):
        previous = sorted_arr[i - 1]
        current = sorted_arr[i]

        if current - previous != 1:
            return previous + 1

    return -1


assert missed_number([5, 3, 7, 8, 2, 4, 9, 6, 0]) == 1


"""
 We want the add the char “z” before each word in the string “alpha”. For example:
dfgalphadss => dfgzalphadss
How will you implement it and what is the complexity of your solution?
"""
# The same task as add_string_into_specific_position

"""
Having an array A, size n, we would like to define an array B, size n as the following: B[i] will be the multiple of all values in A, except A[i].
For example:
A = [2 , 3 , 5]
B = [15, 10, 6]
How will you implement it and what is the complexity of your solution? Please try to provide o(n^2) solution and o(n) solution
"""


def all_products_v1(arr):
    # o(n)
    arr_len = len(arr)
    if arr is None or arr_len == 0 or arr_len == 1:
        return arr

    ans = [1] * arr_len
    for i in range(1, arr_len):
        ans[i] = arr[i - 1] * ans[i - 1]
        right = 1

    for i in range(arr_len - 1, -1, -1):
        ans[i] *= right
        right *= arr[i]

    return ans


def all_products_v2(arr):
    # O(n^2)
    if arr is None or len(arr) == 0:
        return []
    result = []
    arr_len = len(arr)
    for i in range(arr_len):
        for j in range(i + 1, arr_len):
            result.insert(0, arr[i] * arr[j])

    return result


assert all_products_v1([2, 3, 5]) == [15, 10, 6]
assert all_products_v2([2, 3, 5]) == [15, 10, 6]

"""
 Given a positive integer n, please print recursively all digits of n (left to right).
"""


def iterate_digits(n):
    numbers = []

    def recursion(n):
        if n >= 0:
            numbers.insert(0, n)
            iterate_digits(n - 1)

    recursion(n)
    for number in numbers:
        print(number)


iterate_digits(10)

"""
You have an array A[10] with a series of numbers between 0-10 out of order. You need to find out which number is missing. How would you do it?
"""


def missed_number_v1(arr):
    arr_len = len(arr)
    if arr is None or arr_len == 0 or arr_len == 1:
        return arr
    sorted_arr = sorted(arr)

    for i in range(1, arr_len):
        previous = sorted_arr[i - 1]
        current = sorted_arr[i]

        if current - previous != 1:
            return previous + 1

    return -1


assert missed_number([5, 3, 7, 8, 2, 4, 9, 6, 0]) == 1
