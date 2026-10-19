from get_soup import get_soup

def get_player_country(player_id):
    
    "Every player ID starts with the first letter of the family name of the player. So Lebron James id is jamesle01 and the letter we are seaching for is j. That's what this first part of the code does"
    letter=player_id[0]
    
    url=f"https://www.basketball-reference.com/players/{letter}/{player_id}.html"
    
    soup=get_soup(url)
    
    "We earch the href tag for the birthplaces in the table"
    birthplace_cell=soup.find("a", href=lambda href: href and "birthplaces.fcgi" in href)
    
    if birthplace_cell is None:
        return None
    
    "Once we have the url we had before we strip everything that we don't need and search for the actual country code"
    href=birthplace_cell.get("href")
    query_string=href.split("?", 1)[-1]
    params = dict(pair.split("=") for pair in query_string.split("&") if "=" in pair)
    
    
    country_code=params.get("country")
    return country_code.upper() if country_code else None