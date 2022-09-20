import sys
sys.path.append('..')

from onlinemuseum.models import CulturalRelicsData

def run():
    mediums = CulturalRelicsData.objects.values("medium").distinct()
    with open('scripts/medium.txt', 'w') as file:
        sum = 0
        for medium in mediums:
            if medium['medium'] != None:
                count = CulturalRelicsData.objects.filter(medium=medium['medium']).count()
                sum += count
                file.write(medium['medium'] + ' : ' + str(count) + '\n')
        file.write('total' + str(sum) + '\n')
        
        