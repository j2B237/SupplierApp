"""
    Login screen
"""
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen


class LoginScreenView(MDScreen):
    """ Widget rule """

    phone_number = ObjectProperty()
    code_pin = ObjectProperty()

    def on_enter(self, *args):
        self.clear_fields()

    def back_to(self, screen_name):
        """ Back to precede screen """
        self.clear_fields()

        self.manager.transition.direction = "right"
        self.manager.switch_screen(screen_name)

    def on_btn_login_pressed(self):
        print(f'Log in btn pressed')
        # self.manager.transition.direction = "left"
        # self.manager.switch_screen("Login")

    def on_btn_signup_pressed(self):
        """ Take user back to sign up screen view """
        self.manager.transition.direction = "left"
        self.manager.switch_screen("Signup")

    def on_reset_code_pressed(self):
        """ Reset user code pin """
        print(f'Reset code pin')

    def clear_fields(self):
        """ Set empty all form fields """
        self.phone_number.text = ""
        self.code_pin.text = ""
