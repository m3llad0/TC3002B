import curses
from textSimilarityDetector import TextSimilarityDetector

class App:
    """
    A class to represent a console-based application using the curses library.
    """
    def __init__(self, stdscr):
        """Initializes the App with the provided curses window object."""
        self.stdscr = stdscr
        self.current_row = 0
        self.menu = ['Read file', 'Enter Text', 'Exit']
        self.welcome_text = """
 _____         _  ___  ___      _       _               
|_   _|       | | |  \/  |     | |     | |              
  | | _____  _| |_| .  . | __ _| |_ ___| |__   ___ _ __ 
  | |/ _ \ \/ / __| |\/| |/ _` | __/ __| '_ \ / _ \ '__|
  | |  __/>  <| |_| |  | | (_| | || (__| | | |  __/ |   
  \_/\___/_/\_\\__\_|  |_/\__,_|\__\___|_| |_|\___|_|   
                                                        
                                                        """
        self.text_similarity_detector = TextSimilarityDetector('dataset/files')
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
            x = w // 2 - len(line) // 2
            y = idx + 1
            self.stdscr.addstr(y, x, line)

        # Print menu
        for idx, row in enumerate(self.menu):
            x = w // 2 - len(row) // 2
            y = h // 2 + idx  # Adjusting the menu position
            if idx == self.current_row:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, row)
        self.stdscr.refresh()

    def handle_input(self):
        """Handles the user input."""
        key = self.stdscr.getch()

        if key == curses.KEY_UP and self.current_row > 0:
            self.current_row -= 1
        elif key == curses.KEY_DOWN and self.current_row < len(self.menu) - 1:
            self.current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            self.perform_action()

    def perform_action(self):
        """Performs the action corresponding to the current selected menu option."""
        if self.current_row == 0:
            self.option1()
        elif self.current_row == 1:
            self.option2()
        elif self.current_row == 2:
            self.exit_program()

    def option1(self):
        """Performs the action for the first menu option: Check File Similarity."""
        try:
            with open('file.txt', 'r') as file:
                content = file.read()
                result, similarity = self.text_similarity_detector.check_similarity(content)
                self.display_result(result, similarity)
        except FileNotFoundError:
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, "Error: File 'file.txt' not found.")
            self.stdscr.refresh()
            self.stdscr.getch()

    def option2(self):
        """Performs the action for the second menu option: Enter Text and Check Similarity."""
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Enter your text:")
        self.stdscr.refresh()

        user_input = ""
        while True:
            key = self.stdscr.getch()
            if key == curses.KEY_ENTER or key in [10, 13]:
                break
            elif key == curses.KEY_BACKSPACE or key == 127:
                user_input = user_input[:-1]
            else:
                user_input += chr(key)

            self.stdscr.clear()
            self.stdscr.addstr(0, 0, "Enter your text:")
            self.stdscr.addstr(1, 0, user_input)
            self.stdscr.refresh()

        self.stdscr.clear()
        self.stdscr.addstr(0, 0, f"You entered: {user_input}\nChecking similarity...")
        self.stdscr.refresh()
        result, similarity = self.text_similarity_detector.check_similarity(user_input)
        self.display_result(result, similarity)

    def display_result(self, result, similarity):
        """Displays the result of the similarity analysis."""
        h, w = self.stdscr.getmaxyx()
        self.stdscr.clear()

        # Display result
        result_text = f"Result: {result}, Similarity: {similarity:.4f}"
        lines = result_text.split('\n')

        # Determine if scrolling is needed
        if len(lines) > h - 1:  # Subtract 1 for the -- More -- line
            self.stdscr.addstr(h - 1, 0, "-- More --")
            self.stdscr.refresh()
            key = None
            while key not in [curses.KEY_ENTER, 10, 13]:
                key = self.stdscr.getch()
            self.stdscr.clear()

        # Print the result
        for idx, line in enumerate(lines):
            if idx >= h - 1:  # Subtract 1 for the -- More -- line
                break
            self.stdscr.addstr(idx, 0, line)
        self.stdscr.refresh()

        # Wait for user input before returning to the menu
        key = None
        while key not in [curses.KEY_ENTER, 10, 13]:
            key = self.stdscr.getch()

    def exit_program(self):
        """Exits the program."""
        curses.endwin()
        exit()

    def run(self):
        """Runs the application."""
        while True:
            self.print_menu()
            self.handle_input()