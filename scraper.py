import json
import re
import urllib3
import base64


class Scraper:
    def __init__(self):
        self.http = urllib3.PoolManager()
        self.token = self.get_token()

    def join_for_query(self, input_str, join_str):
        return "".join([" " + join_str + s for s in input_str.split(" ")])

    def raw_query(self, search_string, num_items=100):
        request_data = {"projectNames": ["chromium"], "query": search_string,
                        "cannedQuery": 1, "pagination": {"maxItems": num_items}}

        return request_data

    def query_builder(self, with_strings=None, num_items=100, without_strings=None, labels=None, components=None, status=None, reporter=None, owner=None, cc=None, comment_by=None, summary=None):
        query = ""

        if with_strings != None:
            query += self.join_for_query(with_strings, " ")

        if without_strings != None:
            query += self.join_for_query(without_strings, "-")

        if labels != None:
            query += self.join_for_query(labels, "label:")

        if components != None:
            query += self.join_for_query(components, "component:")

        if status != None:
            query += self.join_for_query(status, "status:")

        if reporter != None:
            query += self.join_for_query(reporter, "reporter:")

        if owner != None:
            query += self.join_for_query(owner, "owner:")

        if cc != None:
            query += self.join_for_query(cc, "cc:")

        if comment_by != None:
            query += self.join_for_query(comment_by, "commentby:")

        if summary != None:
            query += self.join_for_query(summary, "summary:")

        query = query.strip()

        request_data = {"projectNames": ["chromium"], "query": query,
                        "cannedQuery": 1, "pagination": {"maxItems": num_items}}

        return request_data

    def get_token(self):
        r = self.http.request(
            'GET', "https://bugs.chromium.org/p/chromium/issues/list")
        response = r.data.decode('utf-8')
        # UGLY, but it works :)
        m = re.search(
            '(?<=[\'"]{1}token[\'"]{1})\s*\:\s*[\'"]{1}(.*)[\'"]{1},', response)
        m = re.search('(?<=[\'"]{1})(.*)([\'"])', m.group(0))
        token = m.group(0)[0:-1]
        return token

    def get_comments(self, loc_id):
        data = json.dumps(
            {'issueRef': {'localId': loc_id, 'projectName': 'chromium'}})

        headers = {
            'authority': 'bugs.chromium.org',
            'accept': 'application/json',
            'x-xsrf-token': self.token,
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'content-type': 'application/json',
            'origin': 'https://bugs.chromium.org'
        }

        r = self.http.request(
            'POST', 'https://bugs.chromium.org/prpc/monorail.Issues/ListComments', headers=headers, body=data)

        response = r.data.decode('utf-8')
        return json.loads(response[5:])

    def download_attachment(self, link):
        headers = {
            'authority': 'bugs.chromium.org',
            'accept': '*/*',
            'x-xsrf-token': self.token,
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'content-type': 'application/json',
            'origin': 'https://bugs.chromium.org'
        }

        url = "https://bugs.chromium.org/p/chromium/issues/attachment" + link

        r = self.http.request('GET', url, headers=headers)
        b6 = base64.b64encode(r.data).decode('utf-8')
        return b6

    def search(self, query):
        data = json.dumps(query)

        headers = {
            'authority': 'bugs.chromium.org',
            'accept': 'application/json',
            'x-xsrf-token': self.token,
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'content-type': 'application/json',
            'origin': 'https://bugs.chromium.org'
        }

        r = self.http.request(
            'POST', 'https://bugs.chromium.org/prpc/monorail.Issues/ListIssues', headers=headers, body=data)

        response = r.data.decode('utf-8')

        return json.loads(response[5:])

    def get_all(self, query):
        ammended_issues = []
        issues = self.search(query)

        for issue in issues['issues']:
            loc_id = issue['localId']
            comments = self.get_comments(loc_id)

            if "comments" in comments:
                for comment in comments['comments']:
                    if "attachments" in comment:
                        for attachment in comment["attachments"]:
                            if "downloadUrl" in attachment:
                                link = attachment['downloadUrl']
                                attachment['data'] = self.download_attachment(
                                    link)
                            elif "viewUrl" in attachment:
                                link = attachment['viewUrl']
                                attachment['data'] = self.download_attachment(
                                    link)

                issue["comments"] = comments["comments"]

            ammended_issues.append(issue)

        return ammended_issues
