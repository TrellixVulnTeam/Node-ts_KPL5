import kivy
from kivy.app import App
from kivy.cache import Cache
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

import networkx as nx

import matplotlib.pyplot as plt

class Nodets(App):
    def build(self):
        self.connecting_node = ""
        main_layout = BoxLayout(orientation='horizontal')

        self.select_edge_popup = Popup(title="Select connecting node")

        controls = BoxLayout(orientation='vertical')
        self.node_textbox = TextInput(multiline=False)
        edge_select = Button(text="Select connecting")
        edge_select.bind(on_press=self.show_popup)
        add_node_button = Button(text="Add Node")
        add_node_button.bind(on_press=self.add_node)
        controls.add_widget(self.node_textbox)
        controls.add_widget(edge_select)
        controls.add_widget(add_node_button)

        self.notes = Image()
        self.G = nx.Graph()

        main_layout.add_widget(controls)
        main_layout.add_widget(self.notes)

        return main_layout

    def add_node(self, instance):
        text = self.node_textbox.text
        if text == "":
            pass
        elif self.connecting_node == "":
            self.G.add_node(text)
        else:
            self.G.add_edge(text, self.connecting_node)
        self.node_textbox.text = ""
        self.render_graph()
        self.show_graph()
        print(self.G.nodes)
        print(text)

    def show_popup(self, instance):
        self.connecting_node = ""

        main_layout = BoxLayout(orientation='vertical')
        root = ScrollView()
        buttons = GridLayout(cols=1, size_hint_y=None)
        btn = ToggleButton(text="", size_hint_y=None, height=80)
        buttons.add_widget(btn)
        for node in self.G.nodes:
            btn = ToggleButton(text=node, size_hint_y=None, height=80)
            btn.bind(on_press=self.set_connect)
            buttons.add_widget(btn)
        root.add_widget(buttons)
        close_button = Button(text='Select node', size_hint=(1,.2))
        close_button.bind(on_press=self.select_edge_popup.dismiss)
        main_layout.add_widget(root)
        main_layout.add_widget(close_button)

        self.select_edge_popup.content = main_layout
        self.select_edge_popup.open()

    def set_connect(self, instance):
        self.connecting_node = instance.text

    def render_graph(self):
        plt.clf()
        nx.draw_networkx(self.G, label=self.G.nodes)
        plt.savefig('graph.png')

    def show_graph(self):
        self.notes.source = 'graph.png'
        self.notes.reload()

if __name__ == "__main__":
    Nodets().run()
