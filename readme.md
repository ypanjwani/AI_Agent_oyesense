This project implements a semi-autonomous web interaction agent that explores a real website, observes its state, makes runtime decisions, performs actions, and produces meaningful insights about website behavior and usability.

Instead of relying on fully scripted automation, the agent is designed to reason about what it sees, adapt its actions dynamically, and stop intentionally when no further meaningful exploration is possible.

The goal of this project is not exhaustive testing, but to demonstrate decision-making, reasoning, and system design in an ambiguous web environment.

--------------Agent Goal------------------

Explore the website like a first-time user, identify meaningful interaction paths, observe page behavior, and surface potential usability or UX issues.

--------------Agent Architecture---------------

The agent follows a simple but powerful loop:
Observe → Decide → Act → Reflect → Stop

-------------Core Components---------------------

1. Observation

Reads the current browser state (page title, URL, links, buttons, products, pagination)

Infers page type (listing vs product)

2. Decision Logic

Chooses the next action at runtime based on observed state

Avoids hard-coded navigation paths

3. Action Execution

Interacts with the browser (click product, go back, stop)

Reflection & Insights

Analyzes pages for missing or confusing interactions

Logs meaningful findings

4. Stopping Logic

Prevents infinite loops

Stops when no new meaningful interactions are available

----------------Decision Logic (High Level)----------------

The agent uses simple heuristics:

If the page is a listing page → open a product

If the page is a product page → return to listing

If a page has already been visited → stop exploration

This keeps behavior adaptive, explainable, and non-scripted

------------Example Exploration Flow------------------

Homepage (listing)
→ Agent detects products
→ Opens a product page
→ Observes lack of interactive CTAs
→ Returns to listing
→ Detects repeated state
→ Stops intentionally

-----------Sample Output----------------

Agent started

--- Step 1 ---
- title: All products | Books to Scrape - Sandbox
- url: https://books.toscrape.com/
- num_links: 94
- num_buttons: 20
- num_products: 20
- has_next_page: True
- page_type: listing
Decision: open_product
Action: Open first product

--- Step 2 ---
- title: A Light in the Attic | Books to Scrape - Sandbox
- url: https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html
- num_links: 4
- num_buttons: 0
- num_products: 0
- has_next_page: False
- page_type: product
Decision: go_back
Action: Go back to listing

--- Step 3 ---
Repeated page detected. Stopping.

Agent finished exploration

Insights Discovered:
- Product page has no interactive buttons; navigation relies on browser controls.

----------How to Run--------------

Setup
pip install playwright
playwright install

Run the Agent
python main.py


The agent will open a browser, explore the website autonomously, and print its reasoning and insights to the console.



