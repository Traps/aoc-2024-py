import argparse
import time
import importlib


from typing import Any, Callable

from . import inputs


def simple_timit(callable:Callable, *args:Any, **kwargs:Any) -> tuple[float, Any]:
    t_start = time.perf_counter()

    result = callable(*args, **kwargs)

    t_end = time.perf_counter()

    return (t_end - t_start, result) 


def main() -> None:
    parser = argparse.ArgumentParser('aoc2024')

    parser.add_argument('day', type=int, choices=range(1,25))
    parser.add_argument('part', type=str, choices=('a', 'b'), default=('a', 'b'), nargs='?')
    parser.add_argument('-s', '--sample', action='store_true')
    parser.add_argument('-c', '--challenge', action='store_true')
    
    args = parser.parse_args()

    challenge_input = None
    
    for part in args.part:
        print(f'Part {part.upper()}:')
        try:
            task_module = importlib.import_module(f'.solutions.day{args.day:02d}{part}', 'aoc2024')
        except ModuleNotFoundError:
            print(f'  Module not found.')
            continue

        if args.sample or not args.challenge:
            sample_inputs = inputs.get_sample_inputs(args.day, part)
    
            for i,sample in enumerate(sample_inputs, 1):
                run_time, result = simple_timit(task_module.solve, sample)

                print(f'  Sample {i} answer: {result} (run time: {run_time:.3f}s)')

        if args.challenge or not args.sample:
            if challenge_input is None:
                challenge_input = inputs.get_challenge_input(args.day)

            run_time, result = simple_timit(task_module.solve, challenge_input)

            print(f'  Challenge answer: {task_module.solve(challenge_input)}  (run time: {run_time:.3f}s)') 


if __name__ == '__main__':
    main()