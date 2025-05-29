### BHS12DTP

# Resources
• code: https://github.com/info-wyf/BHS-12DTP

• Examples: https://opentechschool.github.io/python-flask/core/forms.html

• Learning resources: https://www.w3schools.com/html/html_forms.asp


# Personal Website by Github
• Official guidelines:
```
https://pages.github.com/
https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
```


• Chinese Version:
```
https://lemonchann.github.io/blog/create_blog_with_github_pages/#
```

# Trouble shooting

1.Problem:
remote: Support for password authentication was removed on August 13, 2021.
remote: Please see https://docs.github.com/get-started/getting-started-with-git/about-remote-repositories#cloning-with-https-urls for information on currently recommended modes of authentication.
fatal: Authentication failed for 'https://github.com/info-wyf/BHS-12DTP.git/'

1.Solution:
use GitHub CLI or git-credential-manager:
```
https://docs.github.com/en/get-started/git-basics/caching-your-github-credentials-in-git
```

2.Problem:
```
UndefinedError
jinja2.exceptions.UndefinedError: 'tuple object' has no attribute 'id'
```
2.Solution:
The reason of this problem is your "orders" is a list not an object. Be careful of 
```
# db.row_factory = sqlite3.Row  # Enable dictionary-like access to rows
```

3.Problem:
```
BuildError
werkzeug.routing.exceptions.BuildError: Could not build url for endpoint 'delete' with values ['id']. Did you mean 'delete_order' instead?
```
3.Solution:
The reason of this problem is your "orders" is a list not an object. Be careful of 
```
Always mind the function of url_for('delete'), it needs to bind a function name called delete();
def delete():
```


  
