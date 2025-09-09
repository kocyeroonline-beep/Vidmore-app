from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.list import OneLineListItem
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from plyer import notification
import requests
import threading

# 👇 Hindura iyi link niba uri gukoresha Render/Vercel/Ngrok
SERVER = "https://vidmore-server.onrender.com"

class MainApp(MDApp):
    current_video = None

    def build(self):
        self.theme_cls.primary_palette = "Red"
        return Builder.load_file("main.kv")

    # =========================
    # HOME
    # =========================
    def load_recommended(self):
        """Load trending videos on Home startup"""
        try:
            r = requests.get(f"{SERVER}/trending")
            videos = r.json()
        except Exception as e:
            print("Error:", e)
            videos = []

        layout = self.root.get_screen("home").ids.recommended
        layout.clear_widgets()
        for video in videos:
            card = Builder.template("VideoCard",
                title=video["title"],
                url=video["url"],
                thumbnail_url=video["thumbnail"])
            layout.add_widget(card)

    # =========================
    # SEARCH
    # =========================
    def search_videos(self, query):
        try:
            r = requests.get(f"{SERVER}/search", params={"q": query})
            videos = r.json()
        except:
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

    # =========================
    # PLAY SCREEN
    # =========================
    def show_video(self, video):
        """Erekana kuri PlayScreen"""
        self.current_video = video
        play_box = self.root.get_screen("play").ids.play_box
        play_box.clear_widgets()
        play_box.add_widget(MDLabel(text=video["title"], halign="center"))
        play_box.add_widget(MDLabel(text=video["channel"], halign="center"))
        play_box.add_widget(Image(source=video["thumbnail"], size_hint_y=None, height=200))

        # progress bar
        pb = MDProgressBar(id="progress", value=0, max=100, size_hint_y=None, height="20dp")
        play_box.add_widget(pb)

        # get info streams
        res = requests.get(f"{SERVER}/info", params={"url": video["url"]}).json()
        for s in res["streams"]:
            btn_text = f"{s['type']} {s.get('resolution', s.get('abr',''))}"
            play_box.add_widget(
                OneLineListItem(text=btn_text, on_release=lambda x, itag=s["itag"]: self.start_download(itag))
            )
        self.root.current = "play"

    # =========================
    # DOWNLOAD MANAGER
    # =========================
    def start_download(self, itag):
        """Tangiza download mu thread"""
        threading.Thread(target=self.download, args=(itag,), daemon=True).start()

    def update_progress(self, value, status=None):
        try:
            pb = self.root.get_screen("play").ids.progress
            pb.value = value
            if status:
                toast(status)
        except:
            pass

    def download(self, itag):
        if not self.current_video:
            return

        try:
            toast("Download started...")
            notification.notify(
                title="Vidmore Download",
                message=f"{self.current_video['title']} download started",
                timeout=5
            )

            # Gufata file
            url = f"{SERVER}/download"
            params = {"url": self.current_video['url'], "itag": itag}
            with requests.get(url, params=params, stream=True) as r:
                total = int(r.headers.get("content-length", 0))
                downloaded = 0

                with open("video.mp4", "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            percent = int(downloaded * 100 / total) if total else 0
                            Clock.schedule_once(lambda dt, p=percent: self.update_progress(p, f"Downloading... {p}%"))

            # Finish
            Clock.schedule_once(lambda dt: self.update_progress(100, "Download Complete ✅"))
            toast("Download complete ✅")
            notification.notify(
                title="Vidmore Download",
                message=f"{self.current_video['title']} downloaded successfully",
                timeout=5
            )

        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_progress(0, f"Error: {e}"))
            toast(f"Error: {e}")
            notification.notify(
                title="Vidmore Error",
                message=str(e),
                timeout=5
            )


if __name__ == "__main__":
    MainApp().run()
