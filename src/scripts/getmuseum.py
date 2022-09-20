import sys
sys.path.append('..')

from onlinemuseum.models import CulturalRelicsData

def run():
    museums = CulturalRelicsData.objects.values("museum").distinct()
    with open('scripts/museum.txt', 'w') as file:
        for museum in museums:
            if museum['museum'] != None:
                file.write(museum['museum'] + '\n')