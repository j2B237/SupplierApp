from kivy.core.window import Window

from kivymd.app import MDApp

from View.ManagerScreen.manager_screen import ManagerScreen

# Local import


class SupplierApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (300, 520)
        self.title = "Application Fournisseur de gaz"
        self.theme_cls.material_style = "M2"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "BlueGray"
        self.manager_screen = ManagerScreen()

    def on_start(self):
        """ Initialize database engine before """
        pass

    def build(self) -> ManagerScreen:
        self.manager_screen.add_widget(self.manager_screen.create_screen("Splash"))
        return self.manager_screen


if __name__ == '__main__':
    app = SupplierApp()
    app.run()
