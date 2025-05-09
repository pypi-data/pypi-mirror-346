# SPDX-License-Identifier: MIT
"""gsmcodecs

Register codecs for GSM default 7-bit alphabet
and language-specific shift tables:

   gsm23.038-0-0: GSM default 7-bit alphabet w/ default extension table
   gsm23.038-0-1: GSM default 7-bit alphabet w/ Lang 1 single shift table
   gsm23.038-0-2: GSM default 7-bit alphabet w/ Lang 2 single shift table
   ...
   gsm23.038-0-13: GSM default 7-bit alphabet w/ Lang 13 single shift table
   gsm23.038-1-0: Language id 1 locking shift w/ default extension table
   gsm23.038-1-1: Language id 1 locking shift w/ Lang 1 single shift table
   gsm23.038-1-2: Language id 1 locking shift w/ Lang 2 single shift table
   ...
   gsm23.038-13-13: Language id 13 locking shift w/ Lang 13 single shift table
   gsm23.038: Alias of gsm23.038-0-0

Usage:
	>>> import gsmcodecs
	>>> 'Hello, world'.encode('gsm23.038-0-0')
	b'Hello, world'
	>>> b'Hello, world'.decode('gsm23.038-0-0')
	'Hello, world'

Recognised Language IDs:

    0: Default (6.2.1, 6.2.1.1)
    1: Turkish (A.3.1, A.2.1)
    2: Spanish (A.2.2)
    3: Portugese (A.3.3, A.2.3)
    4: Bengali (A.3.4, A.2.4)
    5: Gujarati (A.3.5, A.2.5)
    6: Hindi (A.3.6, A.2.6)
    7: Kannada (A.3.7, A.2.7)
    8: Malayalam (A.3.8, A.2.8)
    9: Oriya (A.3.9, A.2.9)
    10: Punjabi (A.3.10, A.2.0)
    11: Tamil (A.3.11, A.2.11)
    12: Telugu (A.3.12, A.2.12)
    13: Urdu (A.3.13, A.2.13)

Source: 3GPP TS 23.038 version 18.0.0 Release 18

"""

import codecs

# Character maps are pre-compiled from look-up tables
# see 'lut/README.md' for more details.
from .charmaps import GSMCHARMAPS

_BASENAME = 'gsm23.038'
_ESCAPE = 0x1b  # escape to single shift table
_REPLACE = ord('?')  # '?' is present in all current locking shift tables


class Codec(codecs.Codec):

    def __init__(self, lockId=0, shiftId=0):
        self.lockId = 0
        if lockId in GSMCHARMAPS:
            if 'locking' in GSMCHARMAPS[lockId]:
                self.lockId = lockId
        self.shiftId = 0
        if shiftId in GSMCHARMAPS:
            if 'singleShift' in GSMCHARMAPS[lockId]:
                self.shiftId = shiftId
        self._lockEncode = GSMCHARMAPS[self.lockId]['locking']['encode']
        self._lockDecode = GSMCHARMAPS[self.lockId]['locking']['decode']
        self._shiftEncode = GSMCHARMAPS[self.shiftId]['singleShift']['encode']
        self._shiftDecode = GSMCHARMAPS[self.shiftId]['singleShift']['decode']
        self.name = '%s-%d-%d' % (_BASENAME, self.lockId, self.shiftId)

    def encode(self, input, errors='strict'):
        cnt = 0
        obuf = bytearray()
        for c in input:
            cnt += 1
            cp = ord(c)
            if cp in self._lockEncode:
                obuf.append(self._lockEncode[cp])
            elif cp in self._shiftEncode:
                obuf.extend((_ESCAPE, self._shiftEncode[cp]))
            else:
                if errors == 'ignore':
                    pass
                elif errors == 'replace':
                    obuf.append(self._lockEncode[_REPLACE])
                else:
                    raise UnicodeEncodeError(self.name, input, cnt - 1, cnt,
                                             'unsupported')
        return bytes(obuf), cnt

    def decode(self, input, errors='strict'):
        cnt = 0
        obuf = []
        tbl = self._lockDecode
        for b in input:
            cnt += 1
            if tbl is self._lockDecode and b == _ESCAPE:
                tbl = self._shiftDecode
            else:
                if b in tbl:
                    obuf.append(chr(tbl[b]))
                else:
                    if errors == 'ignore':
                        pass
                    elif errors == 'replace':
                        obuf.append(chr(_REPLACE))
                    else:
                        raise UnicodeDecodeError(self.name, input, cnt - 1,
                                                 cnt, 'unsupported')
                tbl = self._lockDecode
        if tbl is self._shiftDecode:
            if errors == 'ignore':
                pass
            elif errors == 'replace':
                obuf.append(chr(_REPLACE))
            else:
                raise UnicodeDecodeError(self.name, input, cnt - 1, cnt,
                                         'invalid escape')
        return ''.join(obuf), cnt


def makeCodec(lockId=0, shiftId=0):
    codec = Codec(lockId, shiftId)
    return codecs.CodecInfo(codec.encode, codec.decode, name=codec.name)


def findCodec(name):
    codec = None
    if name == _BASENAME:
        codec = makeCodec()
    elif name == 'ucs2':
        # convenience alias ~ encode is suspect
        codec = codecs.lookup('utf-16_be')
    elif name.startswith(_BASENAME):
        cvec = name.split('_')
        if len(cvec) == 3 and cvec[0] == _BASENAME:
            lockId = None
            if cvec[1].isdigit():
                lockId = int(cvec[1])
            shiftId = None
            if cvec[2].isdigit():
                shiftId = int(cvec[2])
            if lockId is not None and shiftId is not None:
                codec = makeCodec(lockId, shiftId)
    return codec


codecs.register(findCodec)
