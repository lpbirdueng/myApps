def removeheader(lines=[], n = 1):
    for i in range(n):
        lines.pop(n-1-i)
    return lines