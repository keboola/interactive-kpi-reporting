#import keboola_api as kb
from kbcstorage.client import Client
import pandas as pd
from jira import JIRA
from jira.resources import Issue
from enum import Enum

def create_or_update(keboola_URL,
                     keboola_key,
                     table_name,
                     bucket_id,
                     file_path,
                     primary_key,
                     is_incremental=False, 
                     delimiter=',',
                     enclosure='"', 
                     escaped_by='', 
                     columns=None,
                     without_headers=False):
    
    client = Client(keboola_URL, keboola_key)
    # check whether a table in the bucket exists. If so, retrieve its table_id
    try:
        try:
            tables = client.tables.list()

        except Exception as e:
            return str(e)
        # there will be 0 or 1 hit
        table_def = list(filter(lambda x: x['bucket']['id']==bucket_id and x['name']==table_name, tables))
        if table_def:
            table_id = table_def[0]['id']
            # table already exists --> load
            try:
                _= client.tables.load(table_id=table_id,
                                    file_path=file_path,
                                    is_incremental=is_incremental, 
                                    delimiter=delimiter,
                                    enclosure=enclosure, 
                                    escaped_by=escaped_by,
                                    columns=columns,
                                    without_headers=without_headers) 
                return f"{table_name} has been updated."
            except Exception as e:
                return str(e)    
        else:
            # table does not exist --> create
            try:
                return client.tables.create(name=table_name,
                                    bucket_id=bucket_id,
                                    file_path=file_path,
                                    primary_key=primary_key) + " successfully created!!"
            except Exception as e:
                return str(e)   
    except Exception as e:
        return str(e)         

def send_slack_notification(client:Client, message:str):
    # 1 mock a dataframe
    rec = [{'channel':'tmp_streamlit_slack', 'text':message}]
    slacktest = pd.DataFrame().from_records(rec)
    slacktest.to_csv("test.csv", index=False)

    # 2 update a table in keboola
    value = create_or_update(client.root_url,
                         client._token,
                         "slack",
                         "in.c-empower_kpis",
                         "test.csv",
                         None,
                         is_incremental=False, 
                         delimiter=',',
                         enclosure='"', 
                         escaped_by='', 
                         columns=None,
                         without_headers=False)
    return value


class IssueType(Enum):
    EPIC = "Epic"
    TASK = "Task"

def init_jira_client(server: str, user_email: str, api_token: str) -> JIRA:
    try:
        jira_options = {'server': server}
        return JIRA(options=jira_options, basic_auth=(user_email, api_token))
    except Exception as jira_exc:
        print(jira_exc)
        print("Failed to authenticate client, please revalidate your email and token")        

def create_new_jira_issue(jira_client: JIRA, issue_type: IssueType, summary: str) -> Issue:

    try:
        issue_num = jira_client.create_issue(project='STR',
                                       #     customfield_10011=epic_name,
                                        summary=summary,
                                        issuetype={'name': issue_type.value}
                                       )
        return f'https://keboola.atlassian.net/jira/software/projects/STR/boards/210?selectedIssue={issue_num} has been created.'
    except Exception as jira_exc:
        print(f"{jira_exc}")
        return(f"Failed to create new {issue_type.value}. Check log for details")
        
