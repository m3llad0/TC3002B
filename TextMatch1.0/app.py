import curses
from textSimilarityDetector import TextSimilarityDetector


class App:
    """
    A class to represent a console-based application using the curses library.

    ...

    Attributes
    ----------
    stdscr : _curses.window
        The main window object where all the action happens.
    current_row : int
        The current selected row in the menu.
    menu : list
        The list of options in the menu.
    welcome_text : str
        The welcome text to display when the application starts.

    Methods
    -------
    setup_curses():
        Sets up the curses environment.
    print_menu():
        Prints the welcome text and the menu.
    handle_input():
        Handles the user input.
    perform_action():
        Performs the action corresponding to the current selected menu option.
    option1():
        Performs the action for the first menu option.
    option2():
        Performs the action for the second menu option.
    exit_program():
        Exits the program.
    run():
        Runs the application.
    """
    def __init__(self, stdscr):
        """Initializes the App with the provided curses window object."""

        self.stdscr = stdscr
        self.current_row = 0
        self.menu = ['Option 1', 'Option 2', 'Exit']
        self.welcome_text = """
         __        __   _                          
         \\ \\      / /__| | ___ ___  _ __ ___   ___ 
          \\ \\ /\\ / / _ \\ |/ __/ _ \\| '_ ` _ \\ / _ \\
           \\ V  V /  __/ | (_| (_) | | | | | |  __/
            \\_/\\_/ \\___|_|\\___\\___/|_| |_| |_|\\___|
        """
        self.setup_curses()

    def setup_curses(self):
        """Sets up the curses environment."""
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def print_menu(self):
        """Prints the welcome text and the menu."""

        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        # Print welcome text
        for idx, line in enumerate(self.welcome_text.splitlines()):
            x = w//2 - len(line)//2
            y = idx + 1
            self.stdscr.addstr(y, x, line)

        # Print menu
        for idx, row in enumerate(self.menu):
            x = w//2 - len(row)//2
            y = h//2 + idx  # Adjusting the menu position
            if idx == self.current_row:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, row)
        self.stdscr.refresh()

    def handle_input(self):
        """Performs the action corresponding to the current selected menu option."""

        key = self.stdscr.getch()

        if key == curses.KEY_UP and self.current_row > 0:
            self.current_row -= 1
        elif key == curses.KEY_DOWN and self.current_row < len(self.menu) - 1:
            self.current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            self.perform_action()

    def perform_action(self):
        """Performs the action for the second menu option."""

        if self.current_row == 0:
            self.option1()
        elif self.current_row == 1:
            self.option2()
        elif self.current_row == 2:
            self.exit_program()

    def option1(self):
        """Performs the action for the first menu option."""

        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        try:
            with open('file.txt', 'r') as file:
                content = file.read()
                self.stdscr.addstr(0, 0, content)
        except FileNotFoundError:
            self.stdscr.addstr(0, 0, "Error: File 'file.txt' not found.")
        self.stdscr.refresh()
        self.stdscr.getch()

    def option2(self):
        """Performs the action for the second menu option."""

        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        self.stdscr.addstr(0, 0, "Enter your text:")
        self.stdscr.refresh()

        user_input = ""
        while True:
            key = self.stdscr.getch()

            if key == curses.KEY_ENTER or key in [10, 13]:
                break
            elif key == curses.KEY_BACKSPACE or key == 127:
                if user_input:
                    user_input = user_input[:-1]
            else:
                user_input += chr(key)

            self.stdscr.clear()
            self.stdscr.addstr(0, 0, "Enter your text:")
            self.stdscr.addstr(1, 0, user_input)
            self.stdscr.refresh()

        self.stdscr.clear()
        self.stdscr.addstr(0, 0, f"You entered: {user_input}")
        self.stdscr.refresh()
        self.stdscr.getch()

    def exit_program(self):
        """Exits the program."""

        curses.endwin()
        exit()

    def run(self):
        """Runs the application."""
        while True:
            self.print_menu()
            self.handle_input()

