import shelve
from pathlib import Path

from django.shortcuts import render


# Create your views here.
def index(request):
    current_sdb_dir = Path(Path.home(), 'sdb')
    topic_slug = 'micropython-esp32'
    title = 'why-emp'
    with shelve.open(str(Path(current_sdb_dir, topic_slug + '.sdb')), flag='r') as db:
        context = db[title]
    return render(request, 'main.html', context)
