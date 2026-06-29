import requests
from bs4 import BeautifulSoup

url = "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

rows = soup.find("table").find_all("tr")

points = []

for row in rows[1:]:  # skip header
    cols = [c.get_text(strip=True) for c in row.find_all("td")]

    if len(cols) == 3:
        x = int(cols[0])
        char = cols[1]
        y = int(cols[2])

        points.append((x, y, char))

max_x = max(x for x, y, c in points)
max_y = max(y for x, y, c in points)

grid = [[" " for _ in range(max_x + 1)]
        for _ in range(max_y + 1)]

for x, y, char in points:
    grid[y][x] = char

for row in grid:
    print("".join(row))