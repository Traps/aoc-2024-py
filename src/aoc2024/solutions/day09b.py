import dataclasses
import itertools


@dataclasses.dataclass(slots=True)
class Void(object):
    addr:int
    size:int

    def insert_file(self, file:'File') -> None:
        file.addr = self.addr

        self.addr += file.size
        self.size -= file.size


@dataclasses.dataclass(slots=True)
class File(Void):
    file_id:int

    @property
    def checksum(self) -> int:
        return sum(self.addr + i for i in range(self.size)) * self.file_id


def parse_disk_map(disk_map:str) -> tuple[list[File], list[Void]]:
    disk_content = map(int, disk_map)
    files, voids = [], []

    try:
        addr = 0
        for file_id in itertools.count(0):
            file_size = next(disk_content)
            
            files.append(File(addr, file_size, file_id))
            
            addr += file_size

            void_size = next(disk_content)
            voids.append(Void(addr, void_size))

            addr += void_size
    
    except StopIteration:
        return files, voids


def defragment_disk(disk_files:list[File], disk_voids:list[Void]) -> None:
    for file in sorted(disk_files, key=lambda f: f.file_id, reverse=True):
        void = next((v for v in disk_voids if v.size >= file.size), None)

        if void is None or void.addr > file.addr:
            continue

        void.insert_file(file)


def solve(_input:str) -> int:
    files, voids = parse_disk_map(_input)

    defragment_disk(files, voids)

    return sum(file.checksum for file in files)