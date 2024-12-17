import pathlib

from typing import Final

SAMPLE_DIR:Final[pathlib.Path] = pathlib.Path(__file__).parent / 'samples'
CHALLENGE_DIR:Final[pathlib.Path] = pathlib.Path(__file__).parent / 'challenges'

def matches_sample(file:pathlib.Path, day:str, part:str) -> bool:
    sample_day = file.stem.split('_')[0]

    if sample_day in (day, day+part):
        return True
    
    return False


def get_sample_inputs(day:str|int, part:str) -> tuple[str]:
    if isinstance(day, int):
        day = f'day{day:02d}'

    sample_files = SAMPLE_DIR.glob(f'{day}*.txt')
    
    sample_files = [file for file in sample_files if matches_sample(file, day, part)]

    sample_files = sorted(sample_files, key=lambda f: f.stem)

    if not sample_files:
        raise KeyError(f'No samples inputs avialable for day: {day}')

    return tuple(f.read_text() for f in sample_files)


def get_challenge_input(day:str|int) -> str:
    if isinstance(day, int):
        day = f'day{day:02d}'

    challenge_file = next(CHALLENGE_DIR.glob(f'{day}*.txt'), None)

    if challenge_file is None:
        raise KeyError(f'No challenge input available for day: {day}')

    return challenge_file.read_text()