from jira import JIRA
from dotenv import load_dotenv
import os
import sys

def dotloader():
    load_dotenv(sys.argv[4])
    jira_user = os.getenv('JIRA_USER')
    jira_pass = os.getenv('JIRA_PASSWORD')
    return jira_user, jira_pass

def set_proxy_environs():
    prox = str("http://wwwcache.sanger.ac.uk:3128")
    os.environ['HTTPS_PROXY'] = prox
    os.environ['HTTP_PROXY'] = prox
    os.environ['https_proxy'] = prox
    os.environ['http_proxy'] = prox

def main():

    set_proxy_environs()
    user, password = dotloader()
    jira = "https://grit-jira.sanger.ac.uk"  # Base url
    auth_jira = JIRA(jira, basic_auth=(user, password))  # Auth

    project = auth_jira.issue(sys.argv[1])
    print(project)

    motif_value = f' {sys.argv[2]}-{sys.argv[3]}'

    project.update(fields={'customfield_10701': motif_value,
                            'customfield_10702' : len(sys.argv[3]) }
                    )

if __name__ == "__main__":
    main()
