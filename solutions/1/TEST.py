from typing import Any


def check_answer(tests: list[dict[Any]], funcname: "function") -> None:
    for i, test in enumerate(tests):
        try:
            test_answer = funcname(test["input"])
            assert test_answer == test["output"], \
                        f'Failed test {i}.\nInput: {tests[i]["input"]}. ' +\
                        f'Output: {tests[i]["output"]}. ' +\
                        f'Your answer: {funcname(tests[i]["input"])}. '
                        
        except Exception as e:
            print(f"\nERROR test {i}.\n{str(e)}\n")
    else:
        print("OK")