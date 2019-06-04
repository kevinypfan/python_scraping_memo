from tube.Spy_tube import Spy_tube
import time

start = time.time()

break_point = []

spy_tube = Spy_tube(need_qty=100)
spyder_videos = spy_tube.search_populate('violeta')
print(len(spyder_videos))
break_point.append(time.time() - start)

spy_tube.download_all(max_workers=6)
break_point.append(time.time() - break_point[-1])

print('爬蟲所花時間: {}'.format(break_point[0]))
print('---------------------------------------')
print('下載所花時間: {}'.format(break_point[1]))
