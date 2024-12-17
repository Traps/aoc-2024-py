import argparse
import importlib

from . import inputs


def main() -> None:
    parser = argparse.ArgumentParser('aoc2024')

    parser.add_argument('day', type=int, choices=range(1,25))
    parser.add_argument('part', type=str, choices=('a', 'b'), default=('a', 'b'), nargs='?')
    parser.add_argument('-s', '--sample', action='store_true')
    parser.add_argument('-c', '--challenge', action='store_true')
    
    args = parser.parse_args()

    challenge_input = inputs.get_challenge_input(args.day)
    
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
                print(f'  Sample {i} answer: {task_module.solve(sample)}')

        if args.challenge or not args.sample:
            print(f'  Challenge answer: {task_module.solve(challenge_input)}') 


if __name__ == '__main__':
    main()