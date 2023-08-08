from .models import Packages

def seed_data():
    package_data = [
        {"title": "Gold", "price": 0, "credit": 0, "benefit": []},
        {"title": "Silver", "price": 0, "credit": 0, "benefit": []},
        {"title": "Copper", "price": 0, "credit": 0, "benefit": []},
    ]
    return package_data

def run_seed():
    data = seed_data()
    for item in data:
        Packages.objects.create(title=item["title"], price=item["price"], credit=item["credit"], benefit=item["benefit"])