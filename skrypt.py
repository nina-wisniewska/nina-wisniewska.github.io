import requests
from bs4 import BeautifulSoup
from googlesearch import search

def pozyskiwanie_opisu(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        description = soup.find('p') # first paragraph 
        length_min = 200 
        if description and len(description.text.strip()) > length_min:
            return description.text.strip()
        else:
            return ""
    except Exception as e:
        return f"Nie udało się pobrać ze strony, błąd {e}"


url_page = "https://www.tiobe.com/tiobe-index/"

response = requests.get(url_page)

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", class_="table table-striped table-top20")

languages = []

# Get list
if table:
    rows = table.find_all("tr")[1:]  # Skip header row
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            position = cols[0].text.strip()
            language = cols[4].text.strip()
            
            img_tag = cols[3].find("img")
            
            img_url = "https://www.tiobe.com" + img_tag['src']
            
            languages.append({"Position": position, "Language": language, "Image": img_url})
else:
    print("Table not found!")
    
    
# Introduction page (index.md)
with open("index.md", "w", encoding="utf-8") as file:
    file.write("# Welcome to the TIOBE Index Report\n\n")
    file.write("This project provides the latest programming language rankings based on the TIOBE Index.\n\n")
    file.write("You can view the full list of languages here:\n\n")
    file.write("[View Programming Language Rankings](tiobe_index.md)\n")

how_many_max = 5
how_many_now = 0

# Main page with list 
with open("tiobe_index.md", "w", encoding="utf-8") as file:
    file.write("# TIOBE Index - Programming Language Popularity\n\n")
    file.write("This is the latest ranking of programming languages from the TIOBE Index.\n\n")
    
    for item in languages:
        img_md = f"![{item['Language']}]({item['Image']})" if item["Image"] else ""
        file.write(f"## {item['Position']}. {item['Language']}\n")
        if img_md:
            file.write("Logo: " f"{img_md}\n\n")
        
        if how_many_now < how_many_max:
            
            lang_filename = f"{item['Language'].replace(' ', '_')}.md"
            
            file.write(f"[View more information here]({lang_filename})\n\n")
            
            with open(lang_filename, "w", encoding="utf-8") as lang_file:
                
                lang_file.write(f"# {item['Language']}")
                if img_md:
                    lang_file.write(f"{img_md}\n\n")
                    
                query = f"{item['Language']} programming language"
                search_results = list(search(query, stop=2)) 
                
                query = f"{item['Language']} programming description"
                results = list(search(query, stop=10))
                
                for i, url in enumerate(results):
                    if pozyskiwanie_opisu(url) == "":
                        continue
                    else:
                        lang_file.write(pozyskiwanie_opisu(url))
                        lang_file.write("\n\n")

                lang_file.write("### Learn More:\n")
                
                for link in search_results:
                    lang_file.write(f"- [More about {item['Language']}]({link})\n")
                
            how_many_now += 1 


print("Markdown files created")


