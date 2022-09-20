"""
    First view when the application start
"""
import os

from kivymd.uix.screen import MDScreen
from kivy.lang import Builder


class SplashScreenView(MDScreen):
    """ Class display splash screen """

    def on_enter(self, *args):
        from os import chdir, getcwd
        current_path = getcwd()

        try:
            chdir(os.path.join(current_path, "instance"))

            if os.path.exists("konse.json"):
                self.manager.switch_screen("fastLogin")
            else:
                Builder.load_string("splash_screen.kv")

        except Exception as e:
            print(f'Splash screen view error log: {e}')
        chdir(current_path)

    def on_btn_signin_pressed(self):
        """ Take user to the login screen """
        self.manager.transition.direction = "left"
        self.manager.switch_screen("Login")

    def on_btn_signup_pressed(self):
        """ Take user to the sign-up screen """
        self.manager.transition.direction = "left"
        self.manager.switch_screen("Signup")

