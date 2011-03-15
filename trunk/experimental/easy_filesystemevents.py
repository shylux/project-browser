import os
import time

def get_state(directory):
    state = {}
    for root, dirs, files in os.walk(directory):
        for f in files:
            path = os.path.join(root, f)
            state[path] = os.path.getmtime(path)
        break  #remove this, and you'll have a recursively directory scan
    return state


watch_dir = os.getcwd() #exchange this for watch an other root directory
cache = get_state(watch_dir) #initial cache building
while True:
    state = get_state(watch_dir)
    for f,m in state.iteritems():
        if cache != state: #something changed
           if cache.keys() == state.keys():
               for f,m in state.iteritems():
                   if m != cache[f]:
                       print "File changed:", f
           else:
               removed = [ f for f in cache.keys() if f not in state.keys() ]
               added = [ f for f in state.keys() if f not in cache.keys() ]
               for f in removed:
                   print "File removed:", f
               for f in added:
                   print "File added:", f
        cache = state
    time.sleep(0.5)
