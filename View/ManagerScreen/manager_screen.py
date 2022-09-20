# OS import
import os

# Kivy import
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import get_color_from_hex

# Kivymd import
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.utils.set_bars_colors import set_bars_colors
from kivymd.color_definitions import colors

# Local import
from View.screens import screens


class ManagerScreen(ScreenManager):
    dialog_wait = None
    rep = False
    _screen_names = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def on_current(self, *args):
        super().on_current(*args)
        self.set_bars_colors(self.app.theme_cls, self.current)

    def set_bars_colors(self, instance_theme_cls, name_screen: str) -> None:
        primary_color = instance_theme_cls.primary_color
        bg_normal = instance_theme_cls.bg_normal

        panel_colors = {
            "Splash": {
                "status_bar_color": primary_color,
                "navigation_bar_color": primary_color,
                "navigation_icon_color": "Light",
            },
        }

        if name_screen in panel_colors:
            set_bars_colors(
                panel_colors[name_screen]["status_bar_color"],
                panel_colors[name_screen]["navigation_bar_color"],
                panel_colors[name_screen]["navigation_icon_color"]
            )

    def create_screen(self, name_screen):
        """ Create new screen from .py file """
        if name_screen not in self._screen_names:
            self._screen_names.append(name_screen)
            self.load_common_package(name_screen)
            exec(f"import View.{screens[name_screen]}")
            self.app.load_all_kv_files(
                os.path.join(self.app.directory, "View", screens[name_screen].split(".")[0])
            )
            view = eval(
                f'View.{screens[name_screen]}.{screens[name_screen].split(".")[0]}View()'
            )
            view.name = name_screen
            return view

    def load_common_package(self, name_screen) -> None:
        """ Load all kv files """
        def _load_kv(path_to_kv):
            kv_loaded = False
            for load_path_kv in Builder.files:
                if path_to_kv in load_path_kv:
                    kv_loaded = True
                    break
            if not kv_loaded:
                if name_screen in ["list"]:
                    from kivy.factory import Factory

                    Factory.register(
                        "OneLineItem",
                        module="View.common.onelinelistitem.one_line_list_item",
                    )
                    Builder.load_file(path_to_kv)

        one_line_list_item_path = os.path.join(
            "View", "common", "onelinelistitem", "one_line_list_item.kv"
        )
        dots_path = os.path.join("View", "common", "dots", "dots.kv")

        if name_screen in ["list"]:
            _load_kv(one_line_list_item_path)
        elif name_screen in ["button", "field"]:
            _load_kv(dots_path)

    def switch_screen(self, screen_name: str) -> None:
        """ Screen to different screen """
        def switch_screen(*args):
            if screen_name not in self._screen_names:
                self.open_dialog()
                screen = self.create_screen(screen_name)
                self.add_screen(screen)

            self.current = screen_name
            self.dialog_wait.dismiss()

        if screen_name not in self._screen_names:
            self.open_dialog()
            Clock.schedule_once(switch_screen)
        else:
            self.current = screen_name

    def switch_screen_to_tab(self,  current_screen, tab_name, transition):
        """ Leave screen for bottom tab """

        try:
            ref_home_screen = self.get_screen(current_screen)
            top_sm = ref_home_screen.ids.top_level_screen_manager
            top_sm.switch_tab(tab_name)
            self.switch_screen(current_screen)
            self.transition.direction = transition

        except AttributeError as e:
            print(f"Error: {e}")

    def open_dialog(self) -> None:
        if not self.dialog_wait:
            image = Image(
                source="assets/images/loading.gif",
                size_hint=(.15, .15),
                pos_hint={"center_x": .5, "center_y": .5},
            )
            self.dialog_wait = ModalView(
                background="assets/images/modal-bg.png",
            )
            self.dialog_wait.add_widget(image)
        self.dialog_wait.open()

    def show_alert_dialog(self, screen_name) -> BooleanProperty:
        """ Show dialog box with two action buttons """
        self.dialog_wait = None
        self.rep = BooleanProperty()

        def on_accept(*args) -> bool:
            """ Perform action when user confirm his choice """
            self.rep = True
            return self.rep

        def on_cancel(*args) -> bool:
            """ Cancel action when user click on this button """
            return self.rep

        if not self.dialog_wait:
            self.dialog_wait = MDDialog(
                text="Etes-vous sur ? ",
                buttons=[
                    MDFlatButton(
                        text="Annuler",
                        theme_text_color="Custom",
                        text_color=self.app.theme_cls.primary_color,
                        on_release=on_cancel
                    ),
                    MDFlatButton(
                        text="Accepter",
                        theme_text_color="Custom",
                        text_color=self.app.theme_cls.primary_color,
                        on_release=on_accept
                    ),
                ],
            )

        self.dialog_wait.open()
        return self.rep

    def add_screen(self, view) -> None:
        """ Add a new screen to screen manager """
        self.add_widget(view)
