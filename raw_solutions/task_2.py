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
