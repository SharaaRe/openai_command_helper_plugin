import requests
from bs4 import BeautifulSoup

base_url = "https://docs.mcneel.com/rhino/5/help/en-us"

# URL of the Rhino 5 command list
url = f"{base_url}/commandlist/command_list.htm"

# Dictionary to store command details
commands_dict = {}

def scrape_command_details():
    # Send a request to the URL
    response = requests.get(url)
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all command elements (You'll need to inspect the HTML structure of the webpage to do this correctly)
    command_elements = soup.find_all(class_="Command_Title")
    # print(command_elements)
    for element in command_elements:
        # Extract command name and URL to command details
        command_url = element.find('a')  # assuming the command name is a link to the command details page
        if command_url:
            command_name = command_url.text.strip()
            command_href = command_url['href']
            full_command_url = f"{base_url}/{command_href[3:]}"

            print(command_name, full_command_url)
            # Fetch command details page
            page = requests.get(full_command_url)
            with open(f'{command_name}.html', 'wb+') as f:
                f.write(page.content)

# Run the scraping function
scrape_command_details()

# Print the result
print(commands_dict.keys())


import pickle


# Open a file in write/append binary mode
with open('commands.pickle', 'wb') as f:

    # Use the dump() method to save the dictionary to the file
    pickle.dump(commands_dict, f)

# Read a dictionary from the file
# with open('commands.pickle', 'rb') as f:

#     # Use the load() method to load the dictionary from the file
#     my_dict = pickle.load(f)