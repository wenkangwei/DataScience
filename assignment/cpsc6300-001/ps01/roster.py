
from bs4 import BeautifulSoup
import requests

def get_team_url(team_id, team_name):
    """
    Get the team URL for a NCAA college football team
    
    Args:
        team_id: the id of a NACC football team assigned by ESPN
        team_name: the name of the football team
        
    Returns:
        team_url: a string representing the URL of the team
    """
    # YOUR CODE HERE
    url = "https://www.espn.com/college-football/team/roster/_/id/"
    team_name = team_name.lower().replace(" ","-")
    url += str(team_id) + '/' + team_name
    return url



def extract_team_roster(team_id, team_name):
    """
    Extract the team roster for a NCAA college football team
    
    Args:
        team_id: the id of a NACC football team assigned by ESPN
        team_name: the name of the football team
        
    Returns:
        a list of dict representing the roster of the entire team.
    """
    roster = []
    import re
    
    def is_player_row(tag):
        if tag.name == 'tr' and tag.has_attr('data-idx'):
            return True
        return False
    
    
    
    # obtain URL
    url = get_team_url(team_id, team_name)
    # Request HTML
    import requests
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    
    #obtain column name of table
    col_names = []
    table = soup.find_all('table')
    t= table[0]
    for c in t.thead.tr.children:
        col_names.append(c.text)
    # Find the list of player ids of each group
    tables = soup.find_all('table')
    for t in tables:
    #     t = soup.find(class_="Table__Title").find_next("table")
        player_id_set = {}
        for tag in t.find_all('a',attrs={"href":re.compile("/player/_/id/[0-9]+/*")} ):
            txt = re.search("/player/_/id/[0-9]*/[a-zA-Z|-]*" ,tag.attrs['href'])
            if txt:
                player_info = txt.group(0).replace("/player/_/id/",'')
                player_info = player_info.split('/')
                player_id, player_name = int(player_info[0]), player_info[1]
                player_name = player_name.replace('-', ' ')
                player_id_set[player_name] = player_id
    #         print(player_id_set)

        # Collect info of each player
        for i, c in enumerate(t.tbody.find_all(is_player_row)):
            tds = c.find_all('td')
            cols = []
            player = {}
            for td in tds:
                cols.append(td.get_text())
    #             print("{}\t{}".format(i, cols))
            name_index = col_names.index('Name')

            # extract player_number from Name
            player_no_re = re.search("\d+", cols[name_index])
            if player_no_re:
                player_no = player_no_re.group(0)
            else:

                player_no = "NA"
#                 print("Name:  ",cols[name_index], "NA")
            # extract alphabetic name from Name
            cols[name_index] = cols[name_index].replace('-',' ')
            cols[name_index] = ''.join(re.findall("[a-zA-Z ]*", cols[name_index]))
            if cols[name_index].lower() in player_id_set.keys():
                player_id = player_id_set[cols[name_index].lower()]
            else:
                player_id = "NA"
                print("Not Found:",  cols[name_index].lower())




            # store the first Defense player info
            player['player_name'] = cols[col_names.index('Name')]
            player['player_id'] = player_id
            player['player_no'] = player_no
            player["POS"] = cols[col_names.index('POS')]
            player['HT'] = cols[col_names.index('HT')]
            player['WT'] = cols[col_names.index('WT')]
            player['Class'] = cols[col_names.index('Class')]
            player['Birthplace'] = cols[col_names.index('Birthplace')]
            roster.append(player)

    return roster
