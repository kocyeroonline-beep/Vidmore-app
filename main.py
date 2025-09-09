from kivy.lang import Builder
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.toast import toast
import requests

# Hinduriye kuri server iri kuri Render
SERVER = "https://vidmore-server.onrender.com"

class MainApp(MDApp):
    current_video = None

    def build(self):
        self.theme_cls.primary_palette = "Red"
        return Builder.load_file("main.kv")

    def on_start(self):
        # Kuva app itangiye, izanye trending kuri Home
        self.load_recommended()

    def load_recommended(self):
        """Load trending videos on Home startup"""
        try:
            r = requests.get(f"{SERVER}/trending")
            videos = r.json()
        except Exception as e:
            print("Trending error:", e)
            videos = []

        layout = self.root.get_screen("home").ids.recommended
        layout.clear_widgets()
        for video in videos:
            card = Builder.template("VideoCard",
                title=video["title"],
                url=video["url"],
                thumbnail_url=video["thumbnail"])
            layout.add_widget(card)

    def search_videos(self, query):
        try:
            r = requests.get(f"{SERVER}/search", params={"q": query})
            videos = r.json()
        except Exception as e:
            print("Search error:", e)
            videos = []

        layout = self.root.get_screen("results").ids.results_grid
        layout.clear_widgets()
        for video in videos:
            card = Builder.template("VideoCard",
                title=video["title"],
                url=video["url"],
                thumbnail_url=video["thumbnail"])
            layout.add_widget(card)
        self.root.current = "results"

    def show_video(self, video):
        """Erekana kuri PlayScreen"""
        self.current_video = video
        play_box = self.root.get_screen("play").ids.play_box
        play_box.clear_widgets()
        play_box.add_widget(OneLineListItem(text=video["title"]))
        play_box.add_widget(OneLineListItem(text=video.get("channel", "")))
        play_box.add_widget(Image(source=video["thumbnail"], size_hint_y=None, height=200))

        try:
            res = requests.get(f"{SERVER}/info", params={"url": video["url"]}).json()
            for s in res.get("streams", []):
                btn_text = f"{s['type']} {s.get('resolution', s.get('abr',''))}"
                play_box.add_widget(
                    OneLineListItem(text=btn_text, on_release=lambda x, itag=s["itag"]: self.download(itag))
                )
        except Exception as e:
            toast(f"Error loading streams: {e}")

        self.root.current = "play"

    def download(self, itag):
        if not self.current_video:
            return
        try:
            requests.get(f"{SERVER}/download", params={"url": self.current_video['url'], "itag": itag})
            toast("Download started...")
        except Exception as e:
            toast(f"Download error: {e}")

if __name__ == "__main__":
    MainApp().run()