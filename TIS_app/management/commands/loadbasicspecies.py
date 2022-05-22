import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from TIS_app.models import Species


class Command(BaseCommand):
    help = "Add tree species to database. Use web scrapping."

    def handle(self, *args, **options):
        html_text = requests.get(
            "https://fiszkoteka.pl/zestaw/405991-drzewa-polsko-lacinskie"
        ).text
        soup = BeautifulSoup(html_text, "lxml")
        div_tag = soup.find_all("div", class_="text")
        i = 0
        while i < len(div_tag):
            one_species = {
                # "polish_name": div_tag[i].text.strip(),
                "latin_name": div_tag[i + 1].text.strip(),
            }
            Species.objects.get_or_create(**one_species)
            i += 2
        print("Added basic tree species to db")
