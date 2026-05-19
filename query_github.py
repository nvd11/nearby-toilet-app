import requests
import json

headers = {
    'Authorization': 'token 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',
    'Accept': 'application/vnd.github.v3+json'
}

# Get user's recent events to see what they did
r = requests.get('https://api.github.com/users/nvd11/events/public', headers=headers)
events = r.json()
print("Events:", len(events))
for e in events[:5]:
    print(e.get('type'), e.get('repo', {}).get('name'), e.get('created_at'))

# Let's also check recently created issues in their repos
r = requests.get('https://api.github.com/search/issues?q=author:nvd11+sort:created-desc', headers=headers)
issues = r.json().get('items', [])
print("Issues:", len(issues))
for i in issues[:5]:
    print("Issue:", i.get('title'), i.get('html_url'))
    
