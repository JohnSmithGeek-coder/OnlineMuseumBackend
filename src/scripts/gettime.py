import sys
sys.path.append('..')

from onlinemuseum.models import CulturalRelicsData

def run():
    timeList = CulturalRelicsData.objects.values("cat2").distinct()
    with open('scripts/out.txt', 'w') as file:
        for time in timeList:
            if time['cat2'] != None:
                count = CulturalRelicsData.objects.filter(cat2=time['cat2']).count()
                file.write(time['cat2'] + ' : ' + str(count) + '\n')