# Advanced Shortcuts - Radial Menu
# Author: Ufuk
# GitHub: github.com/ufuGdev
# Description: A customizable radial menu for Windows shortcuts and programs
# Version: 1.0
# License: MIT

from RadialMenu import RadialMenu
if __name__ == "__main__":
    try:
        menu = RadialMenu()
        menu.run()
    except KeyboardInterrupt:
        print("\nexiting...")
    except Exception as e:
        print(f"error: {e}")
