import sys
sys.path.append('..')

from onlinemuseum.models import CulturalRelicsData

def run():
    times = CulturalRelicsData.objects.values("time_period").distinct()
    with open('scripts/time_priod.txt', 'w') as file:
        for time in times:
            if time['time_period'] != None:
                count = CulturalRelicsData.objects.filter(time_period=time['time_period']).count()
                file.write(time['time_period'] + ' : ' + str(count) + '\n')