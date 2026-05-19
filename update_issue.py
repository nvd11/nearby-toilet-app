import requests

headers = {
    'Authorization': 'token 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',
    'Accept': 'application/vnd.github.v3+json'
}

repo = 'nvd11/cdr-demise-docs'
issue_number = 2

# get the issue
r = requests.get(f'https://api.github.com/repos/{repo}/issues/{issue_number}', headers=headers)
if r.status_code == 200:
    issue = r.json()
    print("Issue found:", issue['title'])
    print("Current body:", issue['body'][:100])
else:
    print("Issue not found:", r.status_code)

