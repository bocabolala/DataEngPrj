from github import Github
import os 

def search_and_save():
    query = 'license:apache-2.0 license:bsd-3-clause license:bsd-2-clause license:gpl license:lgpl license:mit license:mpl-2.0 stars:>=50'
    result = g.search_repositories(query, sort='stars')
 
    print(f'Found {result.totalCount} repo(s)')

    with open('./data.csv', 'w') as f:
        f.write('stars,url,forks,language,size,subscribers,network,issues,watchers,pulls,commits,private,license\n')
        for repo in result:
            try:
                row = f'{repo.stargazers_count},{repo.clone_url},{repo.forks},{repo.language},{repo.size},{repo.subscribers_count},{repo.network_count},{repo.open_issues_count},{repo.watchers_count},{repo.get_pulls().totalCount},{repo.get_commits().totalCount},{repo.private},{repo.get_license().license.name}\n'
                f.write(row)
            except:
                next
    print('Done!')

if __name__ == '__main__':
    token = 'YOUR_TOKEN'
    g = Github(token)
    search_and_save()
