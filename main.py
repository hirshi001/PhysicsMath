
from SITypes import *

MF = MICRO * FARAD
MC = MICRO * COULOMB
def main():
    a1 = 6.22 * MF
    a2 = 6 * MF
    a3 = 2 * MF
    a4 = 8.54 * MF

    b1 = 1 / (1/a1 + 1/a2)
    b2 = 1 / (1/a3 + 1/a4)

    c = b1 + b2

    print(b1.to_string(MF))
    print(b2.to_string(MF))
    print(c.to_string(MF))

    v = 90 * VOLT

    voltageB1 = v
    voltageB2 = v

    chargeB1 = b1 * voltageB1
    chargeB2 = b2 * voltageB2

    chargeA1 = chargeB1
    chargeA2 = chargeB1

    chargeA3 = chargeB2
    chargeA4 = chargeB2

    print(chargeA1.to_string(MC))
    print(chargeA2.to_string(MC))
    print(chargeA3.to_string(MC))
    print(chargeA4.to_string(MC))



    pass
if __name__ == '__main__':
    main()

