import sys
sys.path.append('..')

from onlinemuseum.models import CulturalRelicsData

def run():
    cat1s = CulturalRelicsData.objects.values("cat1").distinct()
    with open('scripts/medium_brief.txt', 'w') as file:
        for cat1 in cat1s:
            if cat1['cat1'] != None:
                count = CulturalRelicsData.objects.filter(cat1=cat1['cat1']).count()
                file.write(cat1['cat1'] + ' : ' + str(count) + '\n')