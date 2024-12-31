import collections
import itertools

from types import NoneType
from typing import Generator, Iterable


def parse_disk_map(disk_map:str) -> Generator[int, None, None]:
    disk_content = map(int, disk_map)

    try:
        for file_id in itertools.count(0):
            for _ in range(next(disk_content)):
                yield file_id

            for _ in range(next(disk_content)):
                yield None
    
    except StopIteration:
        return


def fragment_disk_files(disk_map:Iterable[int|NoneType]) -> Generator[int, None, None]:
    disk_content = collections.deque(disk_map)
    
    try:
        while True:
            head = disk_content.popleft()

            while head is None:
                head = disk_content.pop()

            yield head
    
    except IndexError:
        return


def solve(_input:str) -> int:
    disk_map = parse_disk_map(_input)

    fragmented_files = fragment_disk_files(disk_map)

    return sum(addr*fid for addr,fid in enumerate(fragmented_files))