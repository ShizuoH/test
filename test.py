import tkinter as tk
import paho.mqtt.client as mqtt
import json
import time


class MQTTSubscriber:
    def __init__(self, host, port, topic_filter):
        self.topic_dict = {}
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(host, port)
        self.client.subscribe(topic_filter)
        self.client.loop_start()

    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode("utf-8")
        self.topic_dict[topic] = payload

    def get_topics(self):
        return self.topic_dict


class LogPlayer:
    def __init__(self, log_filename):
        with open(log_filename, "r") as f:
            self.log = json.load(f)

    def play(self, client, start_time):
        for msg in self.log["messages"]:
            if msg["timestamp"] > start_time:
                client.publish(msg["topic_name"], msg["payload"])
                time.sleep(msg["timestamp"] - start_time)
                start_time = msg["timestamp"]

    def get_max_timestamp(self):
        return self.log["messages"][-1]["timestamp"]


class App:
    def __init__(self, master):
        self.master = master
        master.title("MQTTトピック表示ツール")

        # MQTT Subscriberの初期化
        self.subscriber = MQTTSubscriber("localhost", 1883, "#")

        # ログプレイヤーの初期化
        self.log_player = LogPlayer("log.json")
        self.start_time = 0

        # GUI部品の作成
        self.topic_listbox = tk.Listbox(master)
        self.topic_listbox.pack(fill=tk.BOTH, expand=1)
        self.update_button = tk.Button(master, text="トピック更新", command=self.update_topics)
        self.update_button.pack(side=tk.LEFT)
        self.play_button = tk.Button(master, text="ログ再生", command=self.play_log)
        self.play_button.pack(side=tk.LEFT)

        # スライドバーの作成
        self.slider_label = tk.Label(master, text="再生開始時刻")
        self.slider_label.pack()
        self.slider = tk.Scale(master, from_=0, to=self.log_player.get_max_timestamp(), orient=tk.HORIZONTAL, command=self.set_start_time)
        self.slider.pack()

    def update_topics(self):
        topics = self.subscriber.get_topics()
        self.topic_listbox.delete(0, tk.END)
        for topic, payload in topics.items():
            self.topic_listbox.insert(tk.END, f"{topic}: {payload}")

    def play_log(self):
        self.play_button.config(state=tk.DISABLED)
        client = mqtt.Client()
        client.connect("localhost")
        self.log_player.play(client, self.start_time)
        client.disconnect()
        self.play_button.config(state=tk.NORMAL)

    def set_start_time(self, value):
        self.start_time = float(value)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
