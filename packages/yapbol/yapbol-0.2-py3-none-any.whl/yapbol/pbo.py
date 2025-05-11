# -*- coding: utf-8 -*-
# Yet Another PBO Library
# Copyright (C) 2025 Lukasz Taczuk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import functools
import hashlib
import itertools
import struct
import textwrap
from typing import Union, Generator, List, Optional


""" Notes:
https://community.bistudio.com/wiki/PBO_File_Format
PackingMethod; //=0x56657273 Product Entry (resistance/elite/arma)
0x56657273 == 'Vers' in  big-endian ('sreV' in little-endian)

End header (packing method):
0x43707273 == 'Cprs' in  big-endian ('srpC' in little-endian)
"""


def read_asciiz(f) -> Union[str, bytes]:
    toeof = iter(functools.partial(f.read, 1), b'')
    bytestring = b''.join(itertools.takewhile(b'\0'.__ne__, toeof))

    try:
        return bytestring.decode('utf-8')

    except UnicodeDecodeError:
        return bytestring


def write_asciiz(f, string):
    if isinstance(string, str):
        f.write(string.encode('utf-8'))
    else:
        f.write(string)  # Write directly

    f.write(b'\0')


def read_ulong(f) -> int:
    data = f.read(4)
    [ulong] = struct.unpack(b'<L', data)
    return ulong


def write_ulong(f, ulong: int):
    data = struct.pack(b'<L', ulong)
    f.write(data)


class HashingFile:
    def __init__(self, orig_file):
        self.orig_file = orig_file
        self.checksum = hashlib.sha1()

    def write(self, data):
        self.orig_file.write(data)
        self.checksum.update(data)

    def get_hash(self):
        return self.checksum.digest()


class PBOFile:
    def __init__(self, pbo_header: 'PBOHeader', pbo_files: List['PBOFileEntry']):
        self.pbo_header = pbo_header
        self.pbo_files = pbo_files

    @staticmethod
    def read_file(filename) -> 'PBOFile':
        pbo_file_entries = []
        with open(filename, 'rb') as f:
            pbo_header = PBOHeader.parse_from_file(f)

            for header_entry in pbo_header.pbo_entries:
                if header_entry.is_boundary():
                    continue

                pbo_file_entry = PBOFileEntry.parse_from_file(f, header_entry.data_size)

                pbo_file_entries.append(pbo_file_entry)

        pbo_file = PBOFile(pbo_header, pbo_file_entries)

        return pbo_file

    def __str__(self):
        out = str(self.pbo_header) + '\n'

        for f in self.pbo_files:
            out += str(f) + '\n'

        return out

    def save_file(self, filename):
        with open(filename, 'wb') as f:
            hashing_file = HashingFile(f)

            self.pbo_header.save_to_file(hashing_file)

            for pbo_file_entry in self.pbo_files:
                pbo_file_entry.save_to_file(hashing_file)

            f.write(b'\0')
            f.write(hashing_file.get_hash())

    def add_entry(self, filename, data, packing_method=0, original_size=-1, reserved=0, timestamp=0, data_size=-1):
        if data_size == -1:
            data_size = len(data)

        if original_size == -1:
            original_size = data_size

        header_entry = PBOHeaderEntry(filename, packing_method, original_size, reserved, timestamp, data_size)
        file_entry = PBOFileEntry(data, data_size)

        self.pbo_header.pbo_entries.append(header_entry)
        self.pbo_files.append(file_entry)

    def __iter__(self) -> Generator['PBOFileEntryView', None, None]:
        for header_entry, file_entry in zip(self.pbo_header.pbo_entries, self.pbo_files):
            yield PBOFileEntryView(header_entry, file_entry)

    def __getitem__(self, key) -> Union['PBOFileEntryView', Generator['PBOFileEntryView', None, None]]:
        if isinstance(key, int):
            return PBOFileEntryView(self.pbo_header.pbo_entries[key], self.pbo_files[key])

        elif isinstance(key, slice):
            return (PBOFileEntryView(h, f) for h, f in zip(self.pbo_header.pbo_entries[key], self.pbo_files[key]))

        elif isinstance(key, (str, bytes)):
            # Yes, I know it's inefficient. Submit a PR :P
            for entry in self:
                if entry.filename == key:
                    return entry

            raise KeyError('No such file')

        else:
            raise TypeError('Invalid __getitem__ type')


class PBOFileEntryView:
    def __init__(self, header_entry: 'PBOHeaderEntry', file_entry: 'PBOFileEntry'):
        super(PBOFileEntryView, self).__init__()

        self.header_entry = header_entry
        self.file_entry = file_entry

    filename = property(
        fget=lambda self: self.header_entry.filename,
        fset=lambda self, value: setattr(self.header_entry, 'filename', value),
    )
    original_size = property(
        fget=lambda self: self.header_entry.original_size,
        fset=lambda self, value: setattr(self.header_entry, 'original_size', value),
    )
    data = property(
        fget=lambda self: self.file_entry.data,
        fset=lambda self, value: setattr(self.file_entry, 'data', value),
    )

    def __str__(self):
        out = ''
        out += 'Filename: {}\n'.format(self.filename)
        out += 'Size: {}\n'.format(self.original_size)
        out += 'First 100 bytes: {}\n'.format(repr(self.data[:100]))

        return out


class PBOFileEntry:
    def __init__(self, data, physical_size):
        self.data = data
        self.physical_size = physical_size

    @staticmethod
    def parse_from_file(f, length) -> 'PBOFileEntry':
        data = f.read(length)

        pbo_file_entry = PBOFileEntry(data, length)

        return pbo_file_entry

    def __str__(self):
        out = 'PBOFileEntry:\n'
        out += '    Physical size: {}\n'.format(self.physical_size)

        return out

    def save_to_file(self, f):
        f.write(self.data)


class PBOHeader:
    def __init__(
        self,
        header_extension: Optional['PBOHeaderExtension'],
        pbo_entries: List['PBOHeaderEntry'],
        eoh_boundary: 'PBOHeaderEntry',
    ):
        self.header_extension = header_extension
        self.pbo_entries = pbo_entries
        self.eoh_boundary = eoh_boundary

    def __str__(self):
        out = ''

        if self.header_extension:
            out += str(self.header_extension)

        for entry in self.pbo_entries:
            out += str(entry) + '\n'

        out += str(self.eoh_boundary) + '\n'

        return 'PBO Header:\n' + textwrap.indent(out, '    ') + '\n'

    def save_to_file(self, f):
        if not self.pbo_entries:
            return

        if self.header_extension:
            self.header_extension.save_to_file(f)

        for entry in self.pbo_entries:
            entry.save_to_file(f)

        self.eoh_boundary.save_to_file(f)

    @staticmethod
    def parse_from_file(f) -> 'PBOHeader':
        header_entries = []
        header_extension: Optional[PBOHeaderExtension] = None
        eoh_boundary = None
        first_entry = True

        while True:
            pbo_header_entry = PBOHeaderEntry.parse_from_file(f)

            if not pbo_header_entry.is_boundary():
                header_entries.append(pbo_header_entry)

            else:  # If boundary
                if first_entry:
                    # Read header extension
                    header_extension = PBOHeaderExtension.parse_from_file(f, pbo_header_entry)

                else:
                    eoh_boundary = pbo_header_entry
                    break

            first_entry = False

        header = PBOHeader(header_extension, header_entries, eoh_boundary)

        return header


class PBOHeaderExtension:
    def __init__(self, strings, pbo_header_entry: 'PBOHeaderEntry'):
        self.pbo_header_entry = pbo_header_entry
        self.strings = strings

    def __str__(self):
        out = 'PBOHeaderExtension:'
        out += textwrap.indent(str(self.pbo_header_entry), '    ') + '\n'
        for s in self.strings:
            out += '    String: {}\n'.format(s)

        return out

    def save_to_file(self, f):
        self.pbo_header_entry.save_to_file(f)

        for s in self.strings:
            write_asciiz(f, s)

        write_asciiz(f, '')

    @staticmethod
    def parse_from_file(f, pbo_header_entry: 'PBOHeaderEntry') -> 'PBOHeaderExtension':
        strings = []

        while s := read_asciiz(f):
            strings.append(s)

        header_extension = PBOHeaderExtension(strings, pbo_header_entry)

        return header_extension


class PBOHeaderEntry:
    def __init__(self, filename, packing_method, original_size, reserved, timestamp, data_size):
        self.filename = filename
        self.packing_method = packing_method
        self.original_size = original_size
        self.reserved = reserved
        self.timestamp = timestamp
        self.data_size = data_size

    def is_boundary(self):
        return not self.filename

    def __str__(self):
        out = textwrap.dedent(f"""
            PBO Entry:
                filename: {self.filename}
                packing_method: {hex(self.packing_method)}
                original_size: {self.original_size}
                reserved: {self.reserved}
                timestamp: {self.timestamp}
                data_size: {self.data_size}""")

        return out

    def save_to_file(self, f):
        write_asciiz(f, self.filename)
        write_ulong(f, self.packing_method)
        write_ulong(f, self.original_size)
        write_ulong(f, self.reserved)
        write_ulong(f, self.timestamp)
        write_ulong(f, self.data_size)

    @staticmethod
    def parse_from_file(f) -> 'PBOHeaderEntry':
        filename = read_asciiz(f)
        packing_method = read_ulong(f)
        original_size = read_ulong(f)
        reserved = read_ulong(f)
        timestamp = read_ulong(f)
        data_size = read_ulong(f)

        entry = PBOHeaderEntry(filename, packing_method, original_size, reserved, timestamp, data_size)

        return entry
