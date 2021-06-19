from colorama import init, Fore, Back, Style
init()
intro = r"""
---------------------------------------------------------------
                            """+Style.BRIGHT+Fore.CYAN+"HANGMAN"+Style.RESET_ALL+Fore.RESET+"""
---------------------------------------------------------------
                     """+Fore.GREEN+"Welcome to Hangman"+Fore.RESET+"""

"""+Style.DIM+Fore.LIGHTBLUE_EX+"# How to play :-"+Fore.WHITE+"""
    * The computer automatically selects from a list of words.
      
    * It displays the selected word in hyphen's "-".
      example : if the word is "hello", 
                it's displayed as "-----".
                
    * The objective of the game is for the user to guess the
      word selected by the computer.
      
    * You start by guessing an alphabet  if the alphabet is in
      the word then all the occurrence's of the alphabet are
      revealed.
      example : the selected word is "hello"
                Guess the word "-----"
                > l
                You guessed correct
                Guess the word "--ll-"
                > 
    * You have n life's, you loose a life if you guess an
      alphabet that is not in the selected word. If you loose
      all life's you loose the game.
    
    * You should only enter a single alplhabet
      
    * You can change the number of life's and the list of words
      by changing the "Hangman Settings.txt" file
"""+Style.RESET_ALL+Fore.RESET


def list_to_str(lst: list):
    ans = ""
    for i in lst:
        ans += i
    return ans


def find_all_in_str(search_string: str, search_item: str):
    ans = []
    for i, j in enumerate(search_string):
        if j == search_item:
            ans.append(i)
    return ans


def find_all_in_list(search_list: list, search_item: str):
    ans = []
    for i, j in enumerate(search_list):
        if j == search_item:
            ans.append(i)
    return ans


def display_lifes(lifes_left: int,max_lifes: int):
    lost_lifes = max_lifes - lifes_left
    display_lifes_str = Style.BRIGHT+Fore.GREEN+"#"*(lifes_left) + Style.DIM + Fore.RED + "x"*(lost_lifes) + Style.RESET_ALL+Fore.RESET
    return display_lifes_str


def load_settings():
    print(Style.DIM+Fore.YELLOW+"# Loading all the settings"+Fore.RESET+Style.RESET_ALL)
    settings = {}
    settings_file = open("Hangman Settings.txt", "r")
    settings_list = settings_file.readlines()  # reads the file for settings
    settings_file.close()

    for i in range(len(settings_list)-1):
        settings_list[i] = settings_list[i][:-1]  # here we are removing the "/n" from all the line ends

    rem_list = []
    for i, j in enumerate(settings_list):
        if j[0] == "#":
            rem_list.append(i)  # here we are removing the commented lines
    rem_list.sort(reverse=True)
    for i in rem_list:
        settings_list.pop(int(i))

    for i in settings_list:
        each_settings = i.split(" = ")
        settings[each_settings[0]] = each_settings[1]  # here we are making a dictionary of settings

    try:
        settings['max_lifes'] = int(settings['max_lifes'])
    except KeyError:
        return None

    if settings['max_lifes'] < 1:
        return None

    try:
        words_file = open(settings["words_file"], 'r')
        words = words_file.readlines()
        words_file.close()

    except FileNotFoundError:
        return None

    for i in range(len(words)-1):
        words[i] = words[i][:-1]

    settings_final = (settings['max_lifes'], words)
    return settings_final


def reset_settings_file():
    print(Style.DIM+Fore.RED+"* Encountered an error while trying to load settings\n* resetting all the settings to default"+Style.RESET_ALL+Fore.RESET)
    import os
    cur_dir = os.getcwd()
    word_path = cur_dir+"/words.txt"
    default_settings = f"""# add "#" at the start of a new line to stop the program from reading the line.
# don't add empty lines to the text file.
max_lifes = 5
# specify the path to the text file that contains the list of words
words_file = {word_path}
# if you change the any settings here please restart the game."""
    reset_file = open("Hangman Settings.txt", "w")
    reset_file.write(default_settings)
    reset_file.close()


def colorify_display_word(disp_string:str):
    disp_list=list(disp_string)
    for i,j in enumerate(disp_list):
        if j == "-":
            disp_list[i] = Style.DIM+Fore.YELLOW+j+Style.RESET_ALL+Fore.RESET
        else:
            disp_list[i] = Style.BRIGHT+Fore.GREEN+j+Style.RESET_ALL+Fore.RESET
    ret_str = list_to_str(disp_list)
    return ret_str


if __name__ == '__main__':
    from random import randint

    print(intro)
    while True:
        setting = load_settings()
        if setting is None:
            reset_settings_file()
        else:
            print(Style.DIM+Fore.YELLOW+"# Starting the Game"+Fore.RESET+Style.RESET_ALL)
            break
    
    words = setting[1]
    loop = True
    while loop:
        lifes = setting[0]
        selected_index = randint(0, len(words)-1)
        word = words[selected_index]
        words.pop(selected_index)
        revealed = []
        word_list = list(word)
        while lifes > 0:
            if len(set(revealed)) == len(set(word_list)):
                print(f"You Won. The word is \"{Style.BRIGHT}{Fore.GREEN}{word}{Style.RESET_ALL}{Fore.RESET}\"")
                break
            display_word_list = ["-" for i in word_list]
            for i in revealed:
                indexes = find_all_in_list(word_list, i)
                for j in indexes:
                    display_word_list[j] = i
            display_word = colorify_display_word(list_to_str(display_word_list))
            display_current_lifes = display_lifes(lifes,setting[0])
            print(f'lifes: {display_current_lifes}\nThe word to guess is {display_word}\n')
            guessed_item = str(input(f"{Style.BRIGHT}{Fore.BLUE}> {Style.NORMAL}{Fore.YELLOW}"))
            print(Style.RESET_ALL+Fore.RESET,end="")
            if len(guessed_item) != 1 or not guessed_item.isalpha() or (guessed_item not in word_list) or (guessed_item in revealed):
                print(Style.BRIGHT+Fore.RED+"You guessed wrong\n"+Style.RESET_ALL+Fore.RESET)
                lifes -= 1
                continue
            print(Style.BRIGHT+Fore.GREEN+"You guessed correct\n"+Style.RESET_ALL+Fore.RESET)
            revealed.append(guessed_item)

        if lifes < 1:
            print(f"You Lost!! The Word is {Style.BRIGHT}{Fore.RED}{word}{Style.RESET_ALL}{Fore.RESET}")

        if len(words) == 0:
            print("You Completed the game")
            loop = False
            continue

        loop_ask = str(input(f"\nDo You want to play again({Fore.GREEN}yes{Fore.RESET}/{Fore.RED}no{Fore.RESET})\n{Style.BRIGHT}{Fore.BLUE}> {Style.DIM}{Fore.MAGENTA}"))
        if loop_ask.lower() == 'yes':
            print(Style.BRIGHT+Fore.BLUE+"Restarting the Game"+Style.RESET_ALL+Fore.RESET)
            loop = True
        else:
            print(Style.BRIGHT+Fore.BLUE+"\nThank You For Playing"+Style.RESET_ALL+Fore.RESET)
            loop = False
