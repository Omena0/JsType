"""Convert js to only type constructors and type attributes."""

import rjsmin
import sys

def _getNumber(num):
    match num:
        case 0:
            return "Number()"
        case 1:
            return "Number(Boolean(String(Number())))"
        case 2:
            return "Object.is.length"
        case 3:
            return "String(Number.NaN).length"
        case 4:
            return "String.call.name.length"
        case 5:
            return "String.apply.name.length"
        case 6:
            return "String(Number.name).length"
        case 7:
            return "String.valueOf.name.length"
        case 8:
            return "String(Number.POSITIVE_INFINITY).length"
        case 9:
            return "String(Number.z).length"
        case _:
            return f"Object.is.length.toPrecision({getNumber(num-1)}).length"


def getNumber(num):
    result = []
    for i in str(num):
        match int(i):
            case 35:
                i = "String(String().at).length"
            case 38:
                i = "String(Number.isNaN).length"
            case 39:
                i = "String(Number)"
            case _:
                i = _getNumber(int(i))

        result.append(i)

    if len(result) > 1: return f'Number(String().concat({','.join(result)}))'
    else: return result[0]


def getLetter(letter):
    match letter:
        case 'a':
            return f"String().at.name.at()"
        case 'b':
            return f"String().big.name.at()"
        case 'c':
            return f'String.call.name.at()'
        case 'd':
            return f'String(Number.z).at({getNumber(2)})'
        case 'e':
            return f'String(Number.z).at({getNumber(3)})'
        case 'f':
            return f'String(Number.z).at({getNumber(4)})'
        case 'h':
            return f'String.hasOwnProperty.name.at()'

        case _:
            return f'String.fromCharCode({getNumber(ord(letter))})'


def getString(string:str):
    result = []
    for i in string:
        i = getLetter(i)
        result.append(i)

    if len(result) > 1: return f'String(String().concat({','.join(result)}))'
    else: return result[0]


def compile(src:str):
    return f'eval({getString(src)})'


with open(sys.argv[1], 'r') as in_file:
    with open(sys.argv[2], 'w') as out_file:
        out_file.write(compile(rjsmin.jsmin(in_file.read())))
