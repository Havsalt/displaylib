

# -- database
database = {
    "/": "\\",
    "(": ")"
}

# -- mirror database
for key, value in tuple(database.items()):
    database[value] = key

def lookup(letter: str) -> str:
    return database.get(letter, letter)

def flip(line: str) -> str:
    return "".join(database.get(letter, letter) for letter in line)[::-1]

def mapflip(content: list[str]) -> list[str]:
    return [flip(line) for line in content]
