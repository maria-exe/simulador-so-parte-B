from ui.user_interface import SystemInterface
import sys

if __name__ == "__main__":
    system = SystemInterface()
    try:
        system.main_menu()
    except KeyboardInterrupt:
        system.stop()