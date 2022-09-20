import sys
sys.path.append('..')

from onlinemuseum.models import CulturalRelicsData

def run():
    cat3s = CulturalRelicsData.objects.values("cat3").distinct()
    with open('scripts/type.txt', 'w') as file:
        sum = 0
        for cat3 in cat3s:
            if cat3['cat3'] != None:
                count = CulturalRelicsData.objects.filter(cat3=cat3['cat3']).count()
                sum += count
                file.write(cat3['cat3'] + ' : ' + str(count) + '\n')
        file.write('total : ' + str(sum) + '\n')