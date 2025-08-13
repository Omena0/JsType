"""Convert js to only type constructors and type attributes."""

import rjsmin
import sys

def concat(*args):
    args = [arg for arg in args if arg]  # Filter out empty strings
    return f'String().concat({",".join(args)})'

counts = [0]*10
def _getNumber(num):
    counts[num] += 1
    match num:
        case 0:
            return "Number()"
        case 1:
            return "Number.length"
        case 2:
            return "Object.is.length"
        case 3:
            return "Map.name.length"
        case 4:
            return "String(null).length"
        case 5:
            return "Map.apply.name.length"
        case 6:
            return "Number.name.length"
        case 7:
            return "Map.groupBy.name.length"
        case 8:
            return "Map.constructor.name.length"
        case 9:
            return "String(Map.z).length"

def getNumber(num):
    if num in range(10):
        return _getNumber(num)

    match int(num):
        case 34:
            return f"String(String().at).substr({getNumber(1)}).length"
        case 35:
            return "String(String().at).length"
        case 37:
            return 'String(Map.call).length'
        case 38:
            return "String(Number.isNaN).length"
        case 39:
            return "String(Number)"
        case 41:
            return 'String(Map.constructor).length'
        case 46:
            return f'String(Map.propertyIsEnumerable).substr({getNumber(7)}).length'
        case 53:
            return "String(Map.propertyIsEnumerable).length"

    result = []

    for i in str(num):
        i = _getNumber(int(i))

        result.append(i)

    if len(result) > 1:
        result = f'Number({concat(*result)})'
    else:
        result = result[0]

    return result

def getChar(char):
    match char:
        case 'a':
            return f'String().at.name.at()'
        case 'b':
            return f'Map.bind.name.at()'
        case 'c':
            return f'String.call.name.at()'
        case 'd':
            return f'String(Map.z).at({getNumber(2)})'
        case 'e':
            return f'String(Map.z).at({getNumber(3)})'
        case 'f':
            return f'String(Map.z).at({getNumber(4)})'
        case 'g':
            return f'String(Map.groupBy).at({getNumber(9)})'
        case 'h':
            return f'String.hasOwnProperty.name.at()'
        case 'i':
            return f'String(Map.isPrototypeOf).at({getNumber(5)})'
        case 'n':
            return f'String(Map.z).at({getNumber(6)})'
        case 'l':
            return f'String(Map.call).substr({getNumber(9)}).at({getNumber(2)})'
        case '(':
            return f'String(Map).substr({getNumber(9)}).at({getNumber(3)})'
        case ')':
            return f'String(Map).substr({getNumber(9)}).at({getNumber(4)})'
        case 'B':
            return f'Map.bind.name.toUpperCase().at()'
        case ' ':
            return f'String(Map.call).at({getNumber(8)})'
        case 's':
            return 'String.name.at().toLowerCase()'
        case 'o':
            return 'Object.name.toLowerCase().at()'
        case '.':
            return f'String(Number.EPSILON).at({getNumber(1)})'

        case _:
            out =  f'String.fromCharCode({getNumber(ord(char))})'
            print(char, len(out), out)
            return out


def getString(string:str):
    result = []
    for i in string:
        i = getChar(i)
        result.append(i)

    if len(result) > 1: return concat(*result)
    else: return result[0]


def compile(src:str):
    return f'eval({getString(src)})'


with open(sys.argv[1], 'r') as in_file:
    with open(sys.argv[2], 'w') as out_file:
        out = compile(rjsmin.jsmin(in_file.read()))
        print(len(out))
        print(counts)
        out_file.write(out)
