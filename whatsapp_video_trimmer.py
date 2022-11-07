from moviepy.editor import *
from moviepy.video.fx import crop
import os.path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filepath', type=str)
parser.add_argument('-r','--rotate', help='rotate video 90°', action='store_true')
parser.add_argument('-c', '--crop', help='crop video to fit phone screen',action='store_true')
parser.add_argument('-p', '--preview', help='show only preview', action = 'store_true')
parser.add_argument('-d', '--dummy', help='only dummy run', action = 'store_true')
args = parser.parse_args()

# load the video 
path =args.filepath
dir_path = os.path.dirname(path)
clip = VideoFileClip(path)

vid_len = int(clip.duration)
name, ext = clip.filename.split('.')
print(name, ext)
print('length:', vid_len)

secs =  list(range(vid_len+1))
start, end = (input('start time:'), input('end time:'))

if start == '':  start = 0
if (end == '') or (end == 0): end = vid_len
start, end = int(start), int(end)

segment_time = secs[start : end : 30]
# print(segment_time)
fnames = []
for _, k in enumerate(segment_time):
    fn = '%s. %s-%s.%s'%(_+1, name, k, ext)
    y = secs[k: k+30+1]
    print("%s [%s - %s sec]"%(os.path.basename(fn), y[0], y[-1]))
    

segm = input('begin..? how many parts?')
if segm == '': segm = len(segment_time)
else: segm = int(segm)


for k in segment_time[:segm]:
    y = secs[k: k+30+1]
    print(y[0],'-', y[-1])
          
    fn = '%s-%s.%s'%(name, k, ext)
    fnames.append(fn)
    trim = clip.subclip(y[0], y[-1])

    if args.crop:
        w,h = trim.size
        pxx = int((1-(w/1600))*(h/2))
        trim = trim.crop(y1=pxx, y2= h-pxx)
        print('croping %s px from top and bottom'%pxx)
        
    if args.rotate: 
        trim = trim.rotate(270)
        
    if args.preview: trim.preview(audio=False)
    elif args.dummy: continue
    else: trim.write_videofile(fn)
    
for i in fnames:
    print("{} - {:.2f} MB".format(os.path.basename(i), os.path.getsize(i)/(1024*1024)))