from jira import JIRA
from dotenv import load_dotenv
import os
import sys

def dotloader():
    load_dotenv(sys.argv[3])
    jira_user = os.getenv('JIRA_USER')
    jira_pass = os.getenv('JIRA_PASSWORD')
    return jira_user, jira_pass

def set_proxy_environs():
    prox = str("http://wwwcache.sanger.ac.uk:3128")
    os.environ['HTTPS_PROXY'] = prox
    os.environ['HTTP_PROXY'] = prox
    os.environ['https_proxy'] = prox
    os.environ['http_proxy'] = prox
    

def get_contents(file):
    """
    Desc: Gets the only line that should be in the input
            If the non-cannonical = nothing, report only cannonical
            If non-cannonical = something, reorder so cannonical goes first.
    Returns: Motif value.
    """
    
    with open(file) as infile:
        for line in infile:
            contents = line
    
    if contents.split(' & ')[0] == "? - !":
        contents = contents.split(' & ')[1]
    elif contents.split(' & ')[0] == "? - !" and contents.split(' & ')[1] == "! - !":
        contents = '!!!'
    elif contents.contains(' & '):
        contents.split(' & ')
        contents = f'{contents[1]} & {contents[0]}'
    else:
        # Escape for string with only cannonical
        pass

    return contents

def get_length(motif):
    """
    Desc: Gets length of last item in the motif 
            (Should be the cannonical unless only non-cannonical is reported)
            If motif == !!! (this indicates no telo)
    Returns: An int for motif[1] (first motif in list should be cannonical) 
    """
    if motif == '!!!':
        motif_value = 0
    else:
        motif_value = len(motif.split(' - ')[1])
    return int(motif_value)
    


def main():

    set_proxy_environs()
    user, password = dotloader()
    jira = "https://grit-jira.sanger.ac.uk"  # Base url
    auth_jira = JIRA(jira, basic_auth=(user, password))  # Auth

    project = auth_jira.issue(sys.argv[1])

    get_contents(sys.argv[2])

    motif_value = get_contents(sys.argv[2])

    motif_length = get_length(motif_value)

    project.update(fields=  {'customfield_10701': motif_value,
                                'customfield_10702' : motif_length
                            }
                    )

    print( motif_value, motif_length)

if __name__ == "__main__":
    main()
