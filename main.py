# from playwright.sync_api import sync_playwright
# import time


# class WebAgent:
#     def __init__(self, start_url):
#         self.start_url = start_url
#         self.logs = []

#     def log(self, message):
#         print(message)
#         self.logs.append(message)

#     def observe_page(self, page):
#         observations = {}

#         observations["title"] = page.title()
#         observations["url"] = page.url

#         # visible links
#         links = page.locator("a").all()
#         observations["num_links"] = len(links)

#         # visible buttons
#         buttons = page.locator("button").all()
#         observations["num_buttons"] = len(buttons)

#         # product cards (specific to books.toscrape.com)
#         products = page.locator(".product_pod").all()
#         observations["num_products"] = len(products)

#         # pagination
#         next_button = page.locator(".next a")
#         observations["has_next_page"] = next_button.count() > 0

#         return observations

#     def run(self):
#         with sync_playwright() as p:
#             browser = p.chromium.launch(headless=False)
#             context = browser.new_context()
#             page = context.new_page()

#             self.log("Agent started")
#             self.log(f"Opening website: {self.start_url}")

#             page.goto(self.start_url)
#             time.sleep(2)

#             observations = self.observe_page(page)

#             self.log("Page Observations:")
#             for key, value in observations.items():
#                 self.log(f"- {key}: {value}")

#             self.log("Agent finished observation phase")

#             browser.close()


# if __name__ == "__main__":
#     agent = WebAgent("https://books.toscrape.com/")
#     agent.run()



# from playwright.sync_api import sync_playwright
# import time


# class WebAgent:
#     def __init__(self, start_url):
#         self.start_url = start_url
#         self.logs = []

#     def log(self, message):
#         print(message)
#         self.logs.append(message)

#     def observe_page(self, page):
#         observations = {}

#         observations["title"] = page.title()
#         observations["url"] = page.url

#         links = page.locator("a").all()
#         observations["num_links"] = len(links)

#         buttons = page.locator("button").all()
#         observations["num_buttons"] = len(buttons)

#         products = page.locator(".product_pod").all()
#         observations["num_products"] = len(products)

#         next_button = page.locator(".next a")
#         observations["has_next_page"] = next_button.count() > 0

#         return observations

#     def decide_next_action(self, observations):
#         if observations["num_products"] > 0:
#             return "open_product"
#         elif observations["has_next_page"]:
#             return "next_page"
#         else:
#             return "stop"

#     def execute_action(self, page, action):
#         if action == "open_product":
#             self.log("Action: Opening first product")
#             first_product = page.locator(".product_pod h3 a").first
#             first_product.click()
#             time.sleep(2)

#         elif action == "next_page":
#             self.log("Action: Going to next page")
#             page.locator(".next a").click()
#             time.sleep(2)

#         elif action == "stop":
#             self.log("Action: No meaningful action found. Stopping.")

#     def run(self):
#         with sync_playwright() as p:
#             browser = p.chromium.launch(headless=False)
#             context = browser.new_context()
#             page = context.new_page()

#             self.log("Agent started")
#             self.log(f"Opening website: {self.start_url}")

#             page.goto(self.start_url)
#             time.sleep(2)

#             observations = self.observe_page(page)

#             self.log("Initial Page Observations:")
#             for key, value in observations.items():
#                 self.log(f"- {key}: {value}")

#             decision = self.decide_next_action(observations)
#             self.log(f"Decision made: {decision}")

#             self.execute_action(page, decision)

#             new_observations = self.observe_page(page)
#             self.log("Post-Action Page Observations:")
#             for key, value in new_observations.items():
#                 self.log(f"- {key}: {value}")

#             self.log("Agent finished Step 2")

#             browser.close()


# if __name__ == "__main__":
#     agent = WebAgent("https://books.toscrape.com/")
#     agent.run()



from playwright.sync_api import sync_playwright
import time


class WebAgent:
    def __init__(self, start_url, max_steps=5):
        self.start_url = start_url
        self.max_steps = max_steps
        self.logs = []
        self.insights = []
        self.visited_urls = set()

    def log(self, message):
        print(message)
        self.logs.append(message)

    def observe_page(self, page):
        observations = {}

        observations["title"] = page.title()
        observations["url"] = page.url

        observations["num_links"] = page.locator("a").count()
        observations["num_buttons"] = page.locator("button").count()
        observations["num_products"] = page.locator(".product_pod").count()
        observations["has_next_page"] = page.locator(".next a").count() > 0

        # page type inference
        if observations["num_products"] > 0:
            observations["page_type"] = "listing"
        elif "/catalogue/" in observations["url"]:
            observations["page_type"] = "product"
        else:
            observations["page_type"] = "unknown"

        return observations

    def decide_next_action(self, observations):
        page_type = observations["page_type"]

        if page_type == "listing":
            return "open_product"

        if page_type == "product":
            return "go_back"

        return "stop"

    def execute_action(self, page, action):
        if action == "open_product":
            self.log("Action: Open first product")
            page.locator(".product_pod h3 a").first.click()
            time.sleep(2)

        elif action == "go_back":
            self.log("Action: Go back to listing")
            page.go_back()
            time.sleep(2)

        elif action == "stop":
            self.log("Action: Stop exploration")

    def analyze_insights(self, observations):
        if observations["page_type"] == "product" and observations["num_buttons"] == 0:
            self.insights.append(
                "Product page has no interactive buttons; navigation relies on browser controls."
            )

        if observations["page_type"] == "listing" and observations["num_products"] == 0:
            self.insights.append(
                "Listing page contains no products; possible broken state."
            )

    def run(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            self.log("Agent started")
            page.goto(self.start_url)
            time.sleep(2)

            for step in range(self.max_steps):
                self.log(f"\n--- Step {step + 1} ---")

                observations = self.observe_page(page)

                if observations["url"] in self.visited_urls:
                    self.log("Repeated page detected. Stopping.")
                    break

                self.visited_urls.add(observations["url"])

                for key, value in observations.items():
                    self.log(f"- {key}: {value}")

                self.analyze_insights(observations)

                action = self.decide_next_action(observations)
                self.log(f"Decision: {action}")

                if action == "stop":
                    break

                self.execute_action(page, action)

            self.log("\nAgent finished exploration")

            if self.insights:
                self.log("\nInsights Discovered:")
                for insight in set(self.insights):
                    self.log(f"- {insight}")
            else:
                self.log("\nNo significant issues detected")

            browser.close()


if __name__ == "__main__":
    agent = WebAgent("https://books.toscrape.com/")
    agent.run()
