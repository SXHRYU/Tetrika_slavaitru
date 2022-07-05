from TEST import check_answer


tests = [
    {
    "input": [0,2,2,0, 2,2,4,4],
    "output": False
    },
    {
    "input": [0,2,2,0, 1,1,4,4],
    "output": 1
    },
    {
    "input": [1,4,5,1, 2,2,3,3],
    "output": 1
    },
    {
    "input": [-2,2,2,-2, 0,0,3,3],
    "output": 4
    },
    {
    "input": [-4,1,-3,-2, -5,-2,-2,-1],
    "output": 1
    },
    {
    "input": [0,1,1,0, -2,0,-1,1],
    "output": False
    },
    {
    "input": [1,1,-3,-1, 1,1,3,2],
    "output": False
    },
]


# Solution returns False if rectangles touch or not intersect and
# returns area if intersect.

def rectangle_intersect(x1, y1, x2, y2, x3, y3, x4, y4) -> bool | int:
    def are_intersected() -> bool:
        return x2 > x3 and x1 < x4 and y4 > y2 and y3 < y1
    
    def area() -> int:
        width = min (x2, x4) - max(x1, x3)
        height = min(y1, y4) - max(y2, y3)
        return width * height

    if are_intersected():
        return area()
    else:
        return False

check_answer(tests, rectangle_intersect)
