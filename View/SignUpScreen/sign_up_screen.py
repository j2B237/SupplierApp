"""
    Sign up screen view
"""
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen


class SignUpScreenView(MDScreen):
    """ WIdget for sign up screen view """

    phone_number = ObjectProperty()
    code_pin = ObjectProperty()
    username = ObjectProperty()

    def on_enter(self, *args):
        self.clear_fields()

    def back_to(self, screen_name):
        """ Back to precede screen """
        self.clear_fields()

        self.manager.transition.direction = "right"
        self.manager.switch_screen(screen_name)

    def on_btn_login_pressed(self):
        """ Take user back to log in screen view """
        self.manager.transition.direction = "left"
        self.manager.switch_screen("Login")

    def on_btn_signup_pressed(self):
        """ Register and create a new user account """
        print(f'Save user account')

    def clear_fields(self):
        """ Set empty all form fields """
        self.username.text = ""
        self.phone_number.text = ""
        self.code_pin.text = ""
