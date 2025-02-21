# Advanced Shortcuts - Radial Menu
# Author: ufuGdev
# GitHub: github.com/ufugdev
# Description: A customizable radial menu for Windows shortcuts and programs
# Version: 1.0
# License: MIT
# Requirements: pygame, keyboard, pynput
# Inspired by: GTA V's radial menu

import pygame
import json
import math
import keyboard
import win32gui
import win32con
import time
from win32gui import GetCursorPos
from pynput import mouse

class RadialMenu:
    def __init__(self):
        pygame.init()
        # get screen res
        screen_info = pygame.display.Info()
        self.screen_width = screen_info.current_w
        self.screen_height = screen_info.current_h
        
        # Menu size
        self.menu_size = 600
        self.radius = self.menu_size // 3
        self.dead_zone_radius = self.menu_size // 8  # useless middle zone
        
        # Create a transparent window
        self.screen = None
        
        # load config
        with open('config.json', 'r') as f:
            self.config = json.load(f)
            
        self.shortcuts = self.config['shortcuts']
        self.mouse_button = self.config['mouse_button']
        self.selected_option = None
        self.font = pygame.font.Font(None, 24)
        self.menu_visible = False
        self.menu_pos = (0, 0)  #menu position
        
        # Initialize mouse listener
        self.mouse_listener = mouse.Listener(
            on_click=self.on_click,
            on_move=self.on_move
        )
        
    def create_window(self):
        if self.screen is None:
            try:
                self.screen = pygame.display.set_mode((self.menu_size, self.menu_size), pygame.NOFRAME)
                pygame.display.set_caption('Radial Menu')
                
                # transparent
                hwnd = pygame.display.get_wm_info()['window']
                
                def RGB(r, g, b):
                    return r | (g << 8) | (b << 16)
                
                # window style: layered and not in taskbar
                ex_style = (win32con.WS_EX_LAYERED | 
                          win32con.WS_EX_TOOLWINDOW |
                          win32con.WS_EX_TOPMOST)  # Keep topmost while visible
                
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                                     win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | ex_style)
                win32gui.SetLayeredWindowAttributes(hwnd, RGB(0,0,0), 0, win32con.LWA_COLORKEY)
                
                self.center_window()
                return True
            except Exception as e:
                print(f"Error creating window: {e}")
                self.screen = None
                return False
        return True

    def center_window(self):
        if self.screen:
            hwnd = pygame.display.get_wm_info()['window']
            x, y = GetCursorPos()  # Center on cursor position
            x -= self.menu_size // 2
            y -= self.menu_size // 2
            self.menu_pos = (x, y)  # Store menu position
            
            # Position the window
            flags = win32con.SWP_NOACTIVATE | win32con.SWP_SHOWWINDOW
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x, y, 
                                self.menu_size, self.menu_size, 
                                flags)

    def get_angle_to_mouse(self, center, mouse_pos):
        dx = mouse_pos[0] - center[0]
        dy = mouse_pos[1] - center[1]
        angle = math.degrees(math.atan2(-dy, dx))
        if angle < 0:
            angle += 360
        return angle

    def on_move(self, x, y):
        if self.menu_visible:
            #global coordinates to menu coordinates
            menu_x = x - self.menu_pos[0]
            menu_y = y - self.menu_pos[1]
            self.update_selection((menu_x, menu_y))
        return True

    def update_selection(self, mouse_pos):
        if not self.menu_visible:
            return

        center = (self.menu_size // 2, self.menu_size // 2)
        
        #distance from center
        dx = mouse_pos[0] - center[0]
        dy = mouse_pos[1] - center[1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        #if in dead zone
        if distance < self.dead_zone_radius:
            self.selected_option = None
            return
            
        mouse_angle = self.get_angle_to_mouse(center, mouse_pos)
        
        #selected option
        self.selected_option = None
        for option in self.shortcuts:
            angle_diff = (mouse_angle - option['angle'] + 180) % 360 - 180
            if abs(angle_diff) < (360 / len(self.shortcuts)) / 2:
                self.selected_option = option
                break
    
    def draw_menu(self):
        if not self.screen or not self.menu_visible:
            return
            
        try:
            if not pygame.display.get_init():
                self.hide_menu()
                return
                
            self.screen.fill((0, 0, 0))  
            center = (self.menu_size // 2, self.menu_size // 2)
            
            menu_surface = pygame.Surface((self.menu_size, self.menu_size), pygame.SRCALPHA)
            pygame.draw.circle(menu_surface, (40, 40, 40, 160), center, self.radius) 
            pygame.draw.circle(menu_surface, (30, 30, 30, 140), center, self.dead_zone_radius) 
            
            # Get current mouse position relative to menu
            x, y = GetCursorPos()
            menu_x = x - self.menu_pos[0]
            menu_y = y - self.menu_pos[1]
            self.update_selection((menu_x, menu_y))
            
            # Draw options
            for option in self.shortcuts:
                angle = option['angle']
                angle_rad = math.radians(angle)
                
                # Calculate position for the option
                x = center[0] + self.radius * 0.7 * math.cos(angle_rad)
                y = center[1] - self.radius * 0.7 * math.sin(angle_rad)
                
                # Set color based on selection with transparency
                color = (255, 255, 255, 255) if option == self.selected_option else (150, 150, 150, 180)
                
                # Draw the option text
                text = self.font.render(option['name'][:20], True, color)
                text_rect = text.get_rect(center=(x, y))
                menu_surface.blit(text, text_rect)

            self.screen.blit(menu_surface, (0, 0))
            pygame.display.flip()
        except (pygame.error, AttributeError) as e:
            print(f"Draw error: {e}")
            self.hide_menu()

    def execute_command(self, option):
        try:
            # Hide menu before executing command
            self.hide_menu()
            if option['type'] == 'program':
                import subprocess
                subprocess.Popen(option['command'])
            elif option['type'] == 'hotkey':
                # Split the hotkey string
                keys = option['command'].split('+')
                # Press all keys together
                keyboard.press_and_release('+'.join(keys))
        except Exception as e:
            print(f"Error executing command: {e}")
    def on_click(self, x, y, button, pressed):
        # Map button names
        button_name = str(button).replace('Button.', '')
        if button_name == 'x2':
            button_name = 'xbutton2'
        elif button_name == 'x1':
            button_name = 'xbutton1'
            
        # Check if this is our button
        if button_name == self.mouse_button['button']:
            if pressed:
                self.menu_visible = True
                if not self.create_window():
                    self.menu_visible = False
            else:
                if self.menu_visible:
                    selected = self.selected_option  #selected option
                    if selected:
                        self.execute_command(selected)  #hide the menu
                    else:
                        self.hide_menu()
        return True

    def hide_menu(self):
        self.menu_visible = False
        if self.screen:
            try:
                if pygame.display.get_init():
                    hwnd = pygame.display.get_wm_info()['window']
                    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
                    pygame.display.quit()
            except:
                pass  # Ignore errors
            self.screen = None

    def cleanup(self): # Clean up resources before exit
        self.hide_menu()
        self.mouse_listener.stop()
        pygame.quit()

    def run(self):
        try:
            #Start listener
            self.mouse_listener.start()
            
            # Main event loop
            while True:
                if self.menu_visible and self.screen:
                    try:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                raise KeyboardInterrupt
                        self.draw_menu()
                    except pygame.error:
                        self.hide_menu()
                else:
                    time.sleep(0.1)  # Reduce CPU usage
        except KeyboardInterrupt:
            self.cleanup()
        except Exception as e:
            print(f"Error in main loop: {e}")
            self.cleanup()