tests = [
    {
    "data": {"lesson": [1594663200, 1594666800],
             "pupil": [1594663340, 1594663389,
                       1594663390, 1594663395,
                       1594663396, 1594666472],
             "tutor": [1594663290, 1594663430,
                       1594663443, 1594666473]},
    "answer": 3117
    },
    {
    "data": {"lesson": [1594702800, 1594706400],
             "pupil": [1594702789, 1594704500, 
                       1594702807, 1594704542,
                       1594704512, 1594704513,
                       1594704564, 1594705150,
                       1594704581, 1594704582,
                       1594704734, 1594705009, 
                       1594705095, 1594705096,
                       1594705106, 1594706480,
                       1594705158, 1594705773,
                       1594705849, 1594706480,
                       1594706500, 1594706875,
                       1594706502, 1594706503,
                       1594706524, 1594706524,
                       1594706579, 1594706641],
             "tutor": [1594700035, 1594700364, 
                       1594702749, 1594705148,
                       1594705149, 1594706463]},
    "answer": 3577
    },
    {
    "data": {"lesson": [1594692000, 1594695600],
             "pupil": [1594692033, 1594696347],
             "tutor": [1594692017, 1594692066,
                       1594692068, 1594696341]},
    "answer": 3565
    }
]

def listify_times(person_times: list[int], arrive_or_leave: str) -> list[int]:
    """Utility function that returns list of seconds when tutor or pupil
    arrived in class (i % 2 == 0) or left it (i % 2 == 1).
    """
    if arrive_or_leave == "arrive":
        return [value for i, value in enumerate(person_times) if i % 2 == 0]
    elif arrive_or_leave == "leave":
        return [value for i, value in enumerate(person_times) if i % 2 == 1]

def get_first_interval(person_times: list[int], lesson_time: list[int]) -> int:
    """Returns first interval, during which a pupil attended a lesson.
    
    Because a pupil may leave class before the lesson has ended
    (including the very first second of a lesson), we should
    figure out, which interval should be considered first, before which
    no seconds should be counted.

    Binary search was chosen to find this last interval, to avoid
    traversing all the list of pupil's or tutor's times.

    person_times - List of seconds when pupil or tutor arrived (i % 2 == 0)
        in classroom or left it (i % 2 == 1).
    lesson_times - List of seconds when lesson started and finished.
    """
    lesson = lesson_time
    leave_times = listify_times(person_times, "leave")

    left = 0
    right = len(leave_times) - 1
    while left <= right:
        mid = (left + right) // 2
        if (leave_times[mid] > lesson[0] 
            and leave_times[mid-1] > lesson[0] 
            and mid - 1 != -1):
            right = mid - 1
        elif leave_times[mid] < lesson[0]:
            left = mid + 1
        elif leave_times[mid] > lesson[0]:
            return mid

def get_last_interval(person_times: list[int], lesson_time: list[int]) -> int:
    """Returns last interval, during which a pupil attended a lesson.
    
    Because a pupil may arrive in class after the lesson has ended
    (including the very last second of a lesson), we should
    figure out, which interval should be considered last, after which
    no seconds should be counted.

    Binary search was chosen to find this last interval, to avoid
    traversing all the list of pupil's or tutor's times.

    person_times - List of seconds when pupil or tutor arrived (i % 2 == 0)
        in classroom or left it (i % 2 == 1).
    lesson_times - List of seconds when lesson started and finished.
    """
    lesson = lesson_time
    arrival_times = listify_times(person_times, "arrive")
    
    left = 0
    right = len(arrival_times) - 1
    while left <= right:
        mid = (left + right) // 2
        if arrival_times[mid] > lesson[1]:
            right = mid - 1 
        elif mid + 1 < len(arrival_times):
            if (arrival_times[mid] < lesson[1] 
                and arrival_times[mid+1] < lesson[1]):
                left = mid + 1
            elif arrival_times[mid] < lesson[1]:
                return mid
        elif arrival_times[mid] < lesson[1]:
            return mid

def indexify_times(person_times: list[int]) -> list[list[int]]:
    """Utility function that returns list of 
    lists of [arrival, leave] times.

    e.g. given `pupil`:
    person_times = [1594702789, 1594704500, 1594702807, 1594704542, ...]
    turns to [[1594702789, 1594704500], [1594702807, 1594704542], ...]

    This is needed to further settify the range of times.
    
    person_times - List of seconds when pupil or tutor arrived (i % 2 == 0)
        in classroom or left it (i % 2 == 1)
    """
    indexed_list = []
    for i in range(0, len(person_times), 2):
        indexed_list.append([person_times[i], person_times[i+1]])
    return indexed_list

def get_all_times(person_times: list[int]) -> set[int]:
    """Returns a set of all the seconds
    during which a tutor or pupil was in a classroom.
    
    person_times - List of seconds when pupil or tutor arrived (i % 2 == 0)
        in classroom or left it (i % 2 == 1).
        Lesson's seconds are also determined using this method,
        but param's name was left as is to remain constant
        throughout all the functions.
    """
    all_times = set()
    indexed_times = indexify_times(person_times)
    for _, value in enumerate(indexed_times):
        all_times.update(range(value[0], value[1]))
    return all_times

def get_appearance_time(*times) -> int:
    """Returns final seconds count.

    The main idea is we traverse either pupil's time or the tutor's
    and check if either of the corresponding elements are in
    another one's `set()` of seconds.[1] The second condition is that
    the elements should also be in lesson's `set()`, i.e. during
    lesson's time.

    [1] It doesn't matter if we do:
            `for time in pupil_times:
                if time in tutor_times: ...`
        or:
            `for time in tutor_times:
                if time in pupil_times: ...`
        because they give the same intersection.
        But traversing the smaller set should take less time,
        so a check on sets' size was added, thanks to `len()` being O(1).

    *times - Tuple of positional args.
        All pupil seconds should be `times[0]`;
        All tutor seconds should be `times[1]`;
        All lesson seconds should be `times[2]`.
    """
    pupil_times = times[0]
    tutor_times = times[1]
    lesson_times = times[2]
    count = 0
    if len(pupil_times) < len(tutor_times):
        for time in pupil_times:
            if time in tutor_times and time in lesson_times:
                count += 1
    else:
        for time in tutor_times:
            if time in pupil_times and time in lesson_times:
                count += 1
    return count

def appearance(intervals: dict[str, list[int]]) -> int:
    """Main function.
    Returns how many seconds tutor and pupil were in a class simultaneously.

    `pupil_intervals` and `tutor_intervals` have `*2[+2]` in their slices
        to resolve off-by-one errors.
    """
    lesson = intervals["lesson"]
    pupil = intervals["pupil"]
    tutor = intervals["tutor"]

    # Remove unused intervals.
    pupil_intervals = pupil[get_first_interval(pupil, lesson)*2:
                            get_last_interval(pupil, lesson)*2+2]
    tutor_intervals = tutor[get_first_interval(tutor, lesson)*2:
                            get_last_interval(tutor, lesson)*2+2]

    # Transform intervals to seconds.
    pupil_all_times = get_all_times(pupil_intervals)
    tutor_all_times = get_all_times(tutor_intervals)
    lesson_all_times = get_all_times(lesson)

    # Get final result.
    count = get_appearance_time(pupil_all_times,
                                tutor_all_times,
                                lesson_all_times)
    
    return count
    

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test["data"])
        assert test_answer == test["answer"], \
                    f'Error on test case {i}, got {test_answer}, ' +\
                    f'expected {test["answer"]}'
    else:
        print("OK")
