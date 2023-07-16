import os, sys
import subprocess

R = '\033[31m'  # Red
W = '\033[0m'   # White
G = '\033[32m'  # Green
Y = '\033[33m'  # Yellow
L = '\033[90m'  # Grey

try:
    import json
    import time
    from requests import Session
    from concurrent.futures import ThreadPoolExecutor
except ModuleNotFoundError:
    modules = "json time concurrent requests"
    modules = modules.split()
    for module in modules:
        subprocess.run(["pip", "install", module])

class Discord:
    def __init__(self, tokens, super_properties):
        self.tokens = tokens
        self.super_properties = super_properties

        self.banner = """
   ___          ___ __    _____             __
  / _ |__ _____/ (_) /_  / _/ /__  ___  ___/ /
 / __ / // / _  / / __/ / _/ / _ \/ _ \/ _  /
/_/ |_\_,_/\_,_/_/\__/ /_//_/\___/\___/\_,_/
        """

        self.session = Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36",
            "accept": "*/*",
            "accept-language": "en-US",
            "connection": "keep-alive",
            "DNT": "1",
            "origin": "https://discord.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referer": "https://discord.com/channels/@me",
            "TE": "Trailers",
            "X-Super-Properties": self.super_properties
        }

    def send_log_audit(self, token, channel_id, amount, threads, delay):
        for i in range(amount):
            invite_data = {
                "max_age": 86400,
                "max_uses": 1,
                "unique": True
            }
            try:
                sess = self.session.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/invites",
                    headers=self.headers, json=invite_data
                )

                if sess.status_code == 200:
                    print(f"{G}Successfully{W} Sent log {L}{token.split('.')[0]}***{W}")

                elif sess.status_code == 429:
                    print(f"{Y}Ratelimited{W} {token.split('.')[0]}***{W}")
                else:
                    print(f"{R}Failed to send log{W}: {sess.json()['message']}")

                time.sleep(delay)
            
            except Exception as e: print(e)

    def main(self):
        os.system("cls" if os.name == "nt" else "clear")
        print(f"{W}Loaded {len(self.tokens)} tokens\n")
        print(self.banner)
        try:
            self.channel_id = int(input(f"{W}Channel ID:{L} "))
            self.amount = int(input(f"{W}Amount:{L} "))
            self.threads = int(input(f"{W}Threads (1-{len(self.tokens)}):{L} "))
            if self.threads > len(self.tokens):
                self.threads = len(self.tokens)

            elif self.threads < 1:
                self.threads = 1

            self.delay = input(f"{W}Delay int:{L} ")
            if self.delay == "":
                self.delay = 0
            self.delay = int(self.delay)

        except ValueError:
            print("Invalid option, try again")
            time.sleep(2)
            return self.main()

        print("\n\n")

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            for token in self.tokens:
                self.headers.update({"authorization": token})
                executor.submit(self.send_log_audit(
                    token, self.channel_id, 
                    self.amount, self.threads, self.delay
                ))

        print("\nAction finished")
        time.sleep(2)
        sys.exit()

if __name__ == "__main__":
    with open("tokens.txt", "r") as file:
        tokens = file.read().strip().splitlines()

    if len(tokens) < 1:
        print("No tokens in tokens.txt, please insert your tokens")
        sys.exit()

    super_properties = "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
    Start = Discord(tokens, super_properties)
    Start.main()
    
