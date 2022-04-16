"""
@author csgn

REFERENCES:
https://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm
https://en.wikipedia.org/wiki/DES_supplementary_material#Key_Generation
"""

IP: list[list[int]] = [[58, 50, 42, 34, 26, 18, 10, 2],
                       [60, 52, 44, 36, 28, 20, 12, 4],
                       [62, 54, 46, 38, 30, 22, 14, 6],
                       [64, 56, 48, 40, 32, 24, 16, 8],
                       [57, 49, 41, 33, 25, 17,  9, 1],
                       [59, 51, 43, 35, 27, 19, 11, 3],
                       [61, 53, 45, 37, 29, 21, 13, 5],
                       [63, 55, 47, 39, 31, 23, 15, 7]]

PC_1: list[list[int]] = [[57, 49, 41, 33, 25, 17,  9],
                         [1 , 58, 50, 42, 34, 26, 18],
                         [10,  2, 59, 51, 43, 35, 27],
                         [19, 11,  3, 60, 52, 44, 36],
                         [63, 55, 47, 39, 31, 23, 15],
                         [ 7, 62, 54, 46, 38, 30, 22],
                         [14,  6, 61, 53, 45, 37, 29],
                         [21, 13,  5, 28, 20, 12,  4]]

PC_2: list[list[int]] = [[14, 17, 11, 24,  1,  5],
                         [ 3, 28, 15,  6, 21, 10],
                         [23, 19, 12,  4, 26,  8],
                         [16,  7, 27, 20, 13,  2],
                         [41, 52, 31, 37, 47, 55],
                         [30, 40, 51, 45, 33, 48],
                         [44, 49, 39, 56, 34, 53],
                         [46, 42, 50, 36, 29, 32]]

EXPANSION_TABLE: list[list[int]] = [[32,  1,  2,  3,  4,  5],
                                    [ 4,  5,  6,  7,  8,  9],
                                    [ 8,  9, 10, 11, 12, 13],
                                    [12, 13, 14, 15, 16, 17],
                                    [16, 17, 18, 19, 20, 21],
                                    [20, 21, 22, 23, 24, 25],
                                    [24, 25, 26, 27, 28, 29],
                                    [28, 29, 30, 31, 32,  1]]

BIT_ROTATION_TABLE: list[int] = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

S_BOXES = [[[14,  4, 13, 1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9, 0, 7 ],
          	[ 0, 15,  7, 4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5, 3, 8 ],
          	[ 4,  1, 14, 8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10, 5, 0 ],
          	[15, 12,  8, 2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0, 6, 13]],
            
           [[15,  1,  8, 14,  6, 11,  3,  4,  9, 7,  2, 13, 12, 0,  5, 10],
            [ 3, 13,  4,  7, 15,  2,  8, 14, 12, 0,  1, 10,  6, 9, 11,  5],
            [ 0, 14,  7, 11, 10,  4, 13,  1,  5, 8, 12,  6,  9, 3,  2, 15],
            [13,  8, 10,  1,  3, 15,  4,  2, 11, 6,  7, 12,  0, 5, 14,  9]],
   
           [[10,  0,  9, 14, 6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
            [13,  7,  0,  9, 3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
            [13,  6,  4,  9, 8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
            [ 1, 10, 13,  0, 6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]],
       
           [[ 7, 13, 14, 3,  0,  6,  9, 10,  1, 2, 8,  5, 11, 12,  4, 15],
            [13,  8, 11, 5,  6, 15,  0,  3,  4, 7, 2, 12,  1, 10, 14,  9],
            [10,  6,  9, 0, 12, 11,  7, 13, 15, 1, 3, 14,  5,  2,  8,  4],
            [ 3, 15,  0, 6, 10,  1, 13,  8,  9, 4, 5, 11, 12,  7,  2, 14]],
        
           [[ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13, 0, 14,  9],
            [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3, 9,  8,  6],
            [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6, 3,  0, 14],
            [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10, 4,  5,  3]],
       
           [[12,  1, 10, 15, 9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
            [10, 15,  4,  2, 7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
            [ 9, 14, 15,  5, 2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
            [ 4,  3,  2, 12, 9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]],
         
           [[ 4, 11,  2, 14, 15, 0,  8, 13,  3, 12, 9,  7,  5, 10, 6,  1],
            [13,  0, 11,  7,  4, 9,  1, 10, 14,  3, 5, 12,  2, 15, 8,  6],
            [ 1,  4, 11, 13, 12, 3,  7, 14, 10, 15, 6,  8,  0,  5, 9,  2],
            [ 6, 11, 13,  8,  1, 4, 10,  7,  9,  5, 0, 15, 14,  2, 3, 12]],
        
           [[13,  2,  8, 4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
            [ 1, 15, 13, 8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
            [ 7, 11,  4, 1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
            [ 2,  1, 14, 7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]]]


class DES:
    def __init__(self, plain_text: str, key: str):
        self._plain_text = plain_text
        self._key = key
        self._verbose = False

    @property
    def plain_text() -> str:
        return self._plain_text

    @property
    def key() -> str:
        return self._key

    @plain_text.setter
    def plain_text(self, val: str) -> None:
        self._plain_text = plain_text

    @key.setter
    def key(self, val: str) -> None:
        self._key = key

    def toByteArray(self, text: str, *, base: int) -> list[str]:
        return ["{0:04b}".format(int(i, base)) for i in text]

    def __getBitPermutation(self, _bytearray: list[str], bit_table: str):
        table = None

        if bit_table == 'PC_1':
            table = PC_1
        elif bit_table == 'PC_2':
            table = PC_2
        elif bit_table == 'IP':
            table = IP
        elif bit_table == 'E':
            table = EXPANSION_TABLE
        else:
            print(f"{bit_table} does not recognized")
            return

        result: list[str] = []
        text = "".join(_bytearray)
        for row in table:
            k = ""
            for col in row:
                k += text[col-1]
            result.append(k)
        
        return result

    def __shiftCircular(self, _bytearray: list[str]) -> list[list[str]]:
        k = "".join(_bytearray)
        result: list[str] = [k]

        key_list = [i for i in k]
        for index, shiftval in enumerate(BIT_ROTATION_TABLE):
            for j in range(shiftval):
                key_list.append(key_list.pop(0))
            result.append("".join(key_list))
        
        return result

    def __generate16Subkeys(self, _bytearray: list[str]) -> list[list[str]]:
        key_56BitPermutation = self.__getBitPermutation(_bytearray, 'PC_1')

        C0 = key_56BitPermutation[:len(key_56BitPermutation)//2]
        D0 = key_56BitPermutation[len(key_56BitPermutation)//2:]

        C0_Subkeys = self.__shiftCircular(C0)
        D0_Subkeys = self.__shiftCircular(D0)

        key_pairs = list(map(lambda x: "".join(x), zip(C0_Subkeys[1:], D0_Subkeys[1:])))
        key_48BitPermutations = []
        for key_pair in key_pairs:
            key_48BitPermutations.append(self.__splitIntoGroup(self.__getBitPermutation(key_pair, 'PC_2'), block=6))
        
        return key_48BitPermutations

    def __splitIntoGroup(self, _bytearray: list[str], *, block: int):
        k = "".join(_bytearray)

        if len(k) % block != 0:
            print(f"'{k:.16}...' doesn't split into {block} block")
            return

        result = []
        for i in range(0, len(k), block):
            result.append(k[i:i+block])

        return result

    def __feistel(self, _bytearray: list[str], subkey: list[str]):
        return self.__splitIntoGroup(self.__xor(_bytearray, subkey), block=6)

    def __xor(self, _x1, _x2):
        x1 = "".join(_x1)
        x2 = "".join(_x2)
        
        result = []
        for i in range(len(x1)-1, -1, -1):
            result.insert(0, str(int(x1[i]) ^ int(x2[i])))

        return "".join(result)

    def __expansion(self, _bytearray: list[str]):
        return self.__getBitPermutation(_bytearray, 'E')

    def __keyMixing(self, l: list[str], r: list[str], subkey: list[str]):
        expandedL = self.__expansion(l)
        expandedR = self.__expansion(r)

        return r, self.__splitIntoGroup(self.__xor(expandedL, self.__feistel(expandedR, subkey)), block=4)

    def __encode64BitBlockOfData(self, subkeys: list[list[str]]):
        msg_64BitPermutation = self.__splitIntoGroup(self.__getBitPermutation(self.toByteArray(self._plain_text, base=16), 'IP'), block=4)

        l = msg_64BitPermutation[:len(msg_64BitPermutation)//2]
        r = msg_64BitPermutation[len(msg_64BitPermutation)//2:]

        for i in range(16):
            l, r = self.__keyMixing(l, r, subkeys[i])
            print("iteration " + str(i+1))
            print("L: ", *l)
            print("R: ", *r)
 

    def encrypt(self, verbose: bool=False):
        self._verbose = verbose
        
        k = self.__splitIntoGroup(self.toByteArray(self._key, base=16), block=8)
        subkeys = self.__generate16Subkeys(k)
        
        self.__encode64BitBlockOfData(subkeys)

def main():
    plain_text = "0123456789ABCDEF"
    key = "133457799BBCDFF1"

    #M = Text2ByteArray(plain_text, 16)
    #L = M[:len(M)//2]
    #R = M[len(M)//2:]


    des = DES(plain_text, key)
    des.encrypt()
    
    """

    \""" CREATE 16 SUBKEYS, EACH OF WHICH IS 48-BITS LONG \"""
    print(key_48BitPermutations)
    
    \""" ENCODE EACH 64-bit BLOCK OF DATA \"""
    msg_64BitPermutation = Get64BitPermutation("".join(M))
    L = msg_64BitPermutation[:len(msg_64BitPermutation)//2]
    R = msg_64BitPermutation[len(msg_64BitPermutation)//2:]
    
    for i in range(1, 16):
        L, R = R, F(R, key_pairs[i-1])
    """
    

if __name__ == "__main__":
    main()

