def representLine(line):
    result = '\''
    if ':' not in line:
        return ''
    result += line[0:line.find(': ')]
    result += '\': \''
    result += line[line.find(': ') + 2:]
    result += '\',\n'
    return result

if __name__ == '__main__':
    result = '{\n\n'
    while True:
        line = input()
        if line != '':
            representedLine = representLine(line)
            if representedLine != '':
                result += '    ' + representedLine
        else:
            break
    result += '\n}'
    print(result)