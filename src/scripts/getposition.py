import sys
sys.path.append('..')

from onlinemuseum.models import CulturalRelicsData

def run():
    positions = CulturalRelicsData.objects.values("geography").distinct()
    with open('scripts/position.txt', 'w') as file:
        sum = 0
        for position in positions:
            if position['geography'] != None:
                count = CulturalRelicsData.objects.filter(geography=position['geography']).count()
                sum += count
                file.write(position['geography'] + ' : ' + str(count) + '\n')
        file.write('total' + str(sum) + '\n')