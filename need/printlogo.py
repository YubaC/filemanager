import random

logo0=[
    ' _____ __  __ ',
    '|  ___|  \/  |',
    '| |_  | |\/| |',
    '|  _| | |  | |',
    '|_|   |_|  |_|'
]

logo1=[
    '    ___       ___   ',
    '   /\  \     /\__\  ',
    '  /::\  \   /::L_L_ ',
    ' /::\:\__\ /:/L:\__\\',
    ' \/\:\/__/ \/_/:/  /',
    '    \/__/    /:/  / ',
    '             \/__/  '
]

logo2=[
    'OOooOoO Oo      oO ',
    'o       O O    o o ',
    'O       o  o  O  O ',
    'oOooO   O   Oo   O ',
    'O       O        o ',
    'o       o        O ',
    'o       o        O ',
    'O       O        o ',
]

logo3=[
    ' ____                ',
    "/\  _`\   /'\_/`\    ",
    '\ \ \L\_\/\      \   ',
    ' \ \  _\/\ \ \__\ \  ',
    '  \ \ \/  \ \ \_/\ \ ',
    '   \ \_\   \ \_\\\ \_\\',
    '    \/_/    \/_/ \/_/',
]

logo4=[
    ' _______ .___  ___. ',
    '|   ____||   \/   | ',
    '|  |__   |  \  /  | ',
    '|   __|  |  |\/|  | ',
    '|  |     |  |  |  | ',
    '|__|     |__|  |__| '
]

logo5=[
    '@@@@@@@@  @@@@@@@@@@   ',
    '@@@@@@@@  @@@@@@@@@@@  ',
    '@@!       @@! @@! @@!  ',
    '!@!       !@! !@! !@!  ',
    '@!!!:!    @!! !!@ @!@  ',
    '!!!!!:    !@!   ! !@!  ',
    '!!:       !!:     !!:  ',
    ':!:       :!:     :!:  ',
    ' ::       :::     ::   ',
    ' :         :      :    '
]

logo6=[
    'oooooooooooo ooo        ooooo ',
    "`888'     `8 `88.       .888' ",
    " 888          888b     d'888  ",
    ' 888oooo8     8 Y88. .P  888  ',
    " 888          8  `888'   888  ",
    ' 888          8    Y     888  ',
    'o888o        o8o        o888o '
]

logo7=[
    'FFFFFFFFFFFFFFFFFFFFFFMMMMMMMM               MMMMMMMM',
    'F::::::::::::::::::::FM:::::::M             M:::::::M',
    'F::::::::::::::::::::FM::::::::M           M::::::::M',
    'FF::::::FFFFFFFFF::::FM:::::::::M         M:::::::::M',
    '  F:::::F       FFFFFFM::::::::::M       M::::::::::M',
    '  F:::::F             M:::::::::::M     M:::::::::::M',
    '  F::::::FFFFFFFFFF   M:::::::M::::M   M::::M:::::::M',
    '  F:::::::::::::::F   M::::::M M::::M M::::M M::::::M',
    '  F:::::::::::::::F   M::::::M  M::::M::::M  M::::::M',
    '  F::::::FFFFFFFFFF   M::::::M   M:::::::M   M::::::M',
    '  F:::::F             M::::::M    M:::::M    M::::::M',
    '  F:::::F             M::::::M     MMMMM     M::::::M',
    'FF:::::::FF           M::::::M               M::::::M',
    'F::::::::FF           M::::::M               M::::::M',
    'F::::::::FF           M::::::M               M::::::M',
    'FFFFFFFFFFF           MMMMMMMM               MMMMMMMM'
]

logo8=[
    '_|_|_|_|  _|      _|  ',
    '_|        _|_|  _|_|  ',
    '_|_|_|    _|  _|  _|  ',
    '_|        _|      _|  ',
    '_|        _|      _|  '
]

logo9=[
    ' ____  _  _ ',
    '(  __)( \/ )',
    ' ) _) / \/ \\',
    '(__)  \_)(_/'
]

logo10=[
    '    _/_/_/_/  _/      _/   ',
    '   _/        _/_/  _/_/    ',
    '  _/_/_/    _/  _/  _/     ',
    ' _/        _/      _/      ',
    '_/        _/      _/       '
]

def logo():
    global logo0,logo1,logo2,logo3,logo4,logo5,logo6,logo7,logo8,logo9,logo10
    logo=[logo0,logo1,logo2,logo3,logo4,logo5,logo6,logo7,logo8,logo9,logo10]

    return logo[random.randint(0,10)]