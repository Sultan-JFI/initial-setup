import os
import json
import git
from django.core.management.base import BaseCommand
from news.models import NewsArticle, Category 
import tempfile
import shutil

class Command(BaseCommand):
    help = 'Syncs database content to a GitHub repository.'

    def handle(self, *args, **options):
        github_pat = os.environ.get('GITHUB_PAT')
        if not github_pat:
            self.stdout.write(self.style.ERROR('GITHUB_PAT environment variable not found. Cannot proceed.'))
            return

        github_repo_url = "https://github.com/Sultan-JFI/news_site_date-.git"
        
        authenticated_repo_url = github_repo_url.replace("https://", f"https://{github_pat}@")
        
        temp_dir_base = tempfile.gettempdir()
        repo_local_path = os.path.join(temp_dir_base, 'github_export_repo')

        if os.path.exists(repo_local_path):
            self.stdout.write(self.style.NOTICE(f'Removing existing temporary directory: {repo_local_path}'))
            try:
                shutil.rmtree(repo_local_path)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to remove existing directory: {e}'))
                return

        self.stdout.write(self.style.NOTICE(f'Cloning repository into {repo_local_path}...'))
        try:
            repo = git.Repo.clone_from(authenticated_repo_url, repo_local_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clone repository: {e}'))
            return
        
        export_path = os.path.join(repo_local_path, 'data')
        os.makedirs(export_path, exist_ok=True)

        self.stdout.write(self.style.SUCCESS('Repository cloned successfully. Exporting data...'))

        news_articles = NewsArticle.objects.all().values(
            'id', 'title', 'content', 'slug', 'publish_date', 'is_published', 
            'category__name', 'author__username'
        )
        news_data = []
        for article in news_articles:
            if 'publish_date' in article and article['publish_date']:
                article['publish_date'] = article['publish_date'].isoformat()
            news_data.append(article)
        
        with open(os.path.join(export_path, 'news_articles.json'), 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=4)
            
        categories = Category.objects.all().values('id', 'name', 'slug')
        with open(os.path.join(export_path, 'categories.json'), 'w', encoding='utf-8') as f:
            json.dump(list(categories), f, ensure_ascii=False, indent=4)
            
        self.stdout.write(self.style.SUCCESS('Data successfully exported to temporary files.'))

        repo.index.add([os.path.join(export_path, 'news_articles.json'), os.path.join(export_path, 'categories.json')])
        
        if repo.index.diff(repo.head.commit):
            self.stdout.write(self.style.NOTICE('Changes detected. Committing...'))
            repo.index.commit("Automated data sync from Django admin")
            
            origin = repo.remote(name='origin')
            try:
                self.stdout.write(self.style.NOTICE('Pushing changes to GitHub...'))
                origin.push()
                self.stdout.write(self.style.SUCCESS('Data successfully synced to GitHub!'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to push changes to GitHub: {e}'))
        else:
            self.stdout.write(self.style.WARNING('No changes detected. Nothing to commit.'))