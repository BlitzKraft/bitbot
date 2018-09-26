#--require-config google-api-key
#--require-config google-search-id

import json
from src import Utils

URL_GOOGLESEARCH = "https://www.googleapis.com/customsearch/v1"
URL_GOOGLESUGGEST = "http://google.com/complete/search"

class Module(object):
    def __init__(self, bot, events, exports):
        self.bot = bot
        events.on("received.command").on("google", "g").hook(self.google,
            help="Google feeling lucky", usage="[search term]")
        events.on("received.command.suggest").hook(self.suggest,
            help="Get suggested phrases from Google", usage="[phrase]")

    def google(self, event):
        phrase = event["args"] or event["buffer"].get()
        if phrase:
            page = Utils.get_url(URL_GOOGLESEARCH, get_params={
                "q": phrase, "key": self.bot.config[
                "google-api-key"], "cx": self.bot.config[
                "google-search-id"], "prettyPrint": "true",
                "num": 1, "gl": "gb"}, json=True)
            if page:
                if "items" in page and len(page["items"]):
                    event["stdout"].write("(" + Utils.bold(phrase) + ") " \
                                          + page["items"][0]["link"])
                else:
                    event["stderr"].write("No results found")
            else:
                event["stderr"].write("Failed to load results")
        else:
            event["stderr"].write("No phrase provided")

    def suggest(self, event):
        phrase = event["args"] or event["buffer"].get()
        if phrase:
            page = Utils.get_url(URL_GOOGLESUGGEST, get_params={
                "output": "json", "client": "hp", "q": phrase})
            if page:
                # google gives us jsonp, so we need to unwrap it.
                page = page.split("(", 1)[1][:-1]
                page = json.loads(page)
                suggestions = page[1]
                suggestions = [Utils.strip_html(s[0]) for s in suggestions]

                if suggestions:
                    event["stdout"].write("%s: %s" % (phrase,
                        ", ".join(suggestions)))
                else:
                    event["stderr"].write("No suggestions found")
            else:
                event["stderr"].write("Failed to load results")
        else:
            event["stderr"].write("No phrase provided")
