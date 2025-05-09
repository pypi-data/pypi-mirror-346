# gsmcodecs

Python codecs for 3GPP TS 23.038, as used in SMS PDU.

This module provides the GSM default 7-bit alphabet
and language-specific shift tables as python codecs.
A particular pairing of locking shift and single shift
table is chosen by appending the relevant national language IDs
to a base codec 'gsm23.038', separated by dashes (-). Eg:

   - gsm23.038-0-2: GSM default alphabet with Spanish single shift table

Note: These codecs encode and decode one septet per
encoded octet. For GSM style septet packing, refer to related
PDU utilities.

## Usage

	>>> import gsmcodecs
	>>> 'Buenos días'.encode('gsm23.038-0-2')
	b'Buenos d\x1bias'
	>>> b'Buenos d\x1bias'.decode('gsm23.038-0-2')
	'Buenos días'

## Exported Codecs

  - gsm23.038-0-0: GSM 7 bit default alphabet w/ GSM 7 bit default alphabet extension table
  - gsm23.038-X-Y: National language ID X locking shift table w/ National language ID Y single shift table
  - gsm23.038: Alias of gsm23.038-0-0

Note: All possible pairings of locking and single shift tables will return
a codec. In the case that a chosen language ID/table is not defined,
a GSM default table will be substituted. For example,
gsm23.038-2-2 is technically invalid since there is no locking shift
table defined for the Spanish language, the returned codec would be
equivalent to gsm23.038-0-2.

## National Language IDs

The following national language IDs and character mappings
are recognised. Refer to 3GPP TS 23.038, section 6.2 and Annex A:

ID | National Language | Type | Table
--- | --- | --- | ---
0 | Default | GSM default | 6.2.1
0 | Default | Single shift | 6.2.1.1
1 | Turkish | Locking shift | A.3.1
1 | Turkish | Single shift | A.2.1
2 | Spanish | Single shift | A.2.2
3 | Portugese | Locking shift | A.3.3
3 | Portugese | Single shift | A.2.3
4 | Bengali | Locking shift | A.3.4
4 | Bengali | Single shift | A.2.4
5 | Gujarati | Locking shift | A.3.5
5 | Gujarati | Single shift | A.2.5
6 | Hindi | Locking shift | A.3.6
6 | Hindi | Single shift | A.2.6
7 | Kannada | Locking shift | A.3.7
7 | Kannada | Single shift | A.2.7
8 | Malayalam | Locking shift | A.3.8
8 | Malayalam | Single shift | A.2.8
9 | Oriya | Locking shift | A.3.9
9 | Oriya | Single shift | A.2.9
10 | Punjabi | Locking shift | A.3.10
10 | Punjabi | Single shift | A.2.10
11 | Tamil | Locking shift | A.3.11
11 | Tamil | Single shift | A.2.11
12 | Telugu | Locking shift | A.3.12
12 | Telugu | Single shift | A.2.12
13 | Urdu | Locking shift | A.3.13
13 | Urdu | Single shift | A.2.13

CSV source files for each table are located under the 'lut/' directory.

## Re-building Character Maps

Character maps for each of the default and national
language tables can be re-computed from the source CSV
files in the lut directory:

	$ cd lut
	$ make clean && make

## Installation

	$ pip install gsmcodecs
