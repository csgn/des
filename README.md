# DES Implementation

## Options

```bash
options:
  -h, --help            show this help message and exit
  --text TEXT           Enter a text
  --key KEY             Enter a key
  --mode encrypt | decrypt
                        encrypt=0, decrypt=1
```

## Usage

### Encryption
```bash
$ python des.py --text "123456ABCD132536" --key "AABB09182736CCDD" --mode 0

output: 
	ENCRYPT: 123456ABCD132536 ==> C0B7A8D05F3A829C
```

### Decryption
```bash
$ python des.py --text "C0B7A8D05F3A829C" --key "AABB09182736CCDD" --mode 1

output:
	DECRYPT: C0B7A8D05F3A829C ==> 123456ABCD132536
```
