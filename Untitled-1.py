string = """[3/13/2025 4:04 PM] Juan Avendaño: 14.5
[3/13/2025 4:04 PM] Juan Avendaño: 14.52
[3/13/2025 4:05 PM] Juan Avendaño: 14.5
[3/13/2025 4:06 PM] Juan Avendaño: 14.48
[3/13/2025 4:07 PM] Juan Avendaño: 14.72
[3/13/2025 4:16 PM] Juan Avendaño: 14.64
[3/13/2025 4:17 PM] Juan Avendaño: 14.2
[3/13/2025 4:17 PM] Juan Avendaño: 14.72
[3/13/2025 4:17 PM] Juan Avendaño: 14.32
[3/13/2025 4:17 PM] Juan Avendaño: 14.66
[3/13/2025 4:17 PM] Juan Avendaño: 14.7
[3/13/2025 4:17 PM] Juan Avendaño: 14.64
[3/13/2025 4:17 PM] Juan Avendaño: 14.32
[3/13/2025 4:17 PM] Juan Avendaño: 14.6
[3/13/2025 4:18 PM] Juan Avendaño: 14.5"""

string = string.split("\n")
strings = ""
vars = []
for i in range(1, 16):
    
    var = string[i-1][string[i-1].index("ñ")+4:]
    vars.append(float(var))
    strings += var.strip() + " "
    if i % 3 == 0:
        strings += "\n"

print(strings)
print(vars)