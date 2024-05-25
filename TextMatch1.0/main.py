import curses
from app import App

def main(stdscr):
    app = App(stdscr)
    app.run()

    




if __name__ == '__main__':
    curses.wrapper(main)
    main()
