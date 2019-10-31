#!/bin/bash
# lock so the process runs only once at a time
[ "${FLOCKER}" != "$0" ] && exec env FLOCKER="$0" flock -en "$0" "$0" "$@" || : 

date
trap 'trap - SIGINT; kill -SIGINT $$' SIGINT;
date=$(echo "$1" | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
if [  -z "$date" ]; then
  date=$(date -u -d "now - 15 minutes" +%F)
fi
IFS='-' read -r -a dateparts <<< $date
year="${dateparts[0]}"
month="${dateparts[1]}"
day="${dateparts[2]}"
date="$year/$month/$day"
v=aja-helo-1H000314
folder=/opt/data/spidvid/video/$v
dname=$folder/$date
updates=0
if [ ! -d $dname ]; then
  echo $dname not found >&2
  exit 1;
fi
echo $dname
for mp4 in $dname/${v}*.mp4
do
  fname=$(basename $mp4)
  t1=$(echo $fname | sed -e "s/${v}_//" -e 's/.mp4$//' -e 's/_/ /' -e 's/\(..\)\(..\)$/\1:\2:00/')
  t1=$(date -d "$t1" -u +%FT%TZ)
  t2=$(date -d "$t1 + 1 minute" -u +%FT%TZ)
  s1=$(echo $t1 | sed -e 's/:/\\:/g') # -e 's/T/ /' -e 's/Z//')
  s2=$(echo $t2 | sed -e 's/:/\\:/g') # -e 's/T/ /' -e 's/Z//')
  p1=$dname/${v}_$(echo $t1 | sed -e 's/T/_/' -e 's/:00Z$/.png/' -e 's/://')
  p2=$dname/${v}_$(echo $t2 | sed -e 's/T/_/' -e 's/:00Z$/.png/' -e 's/://')
  test -f $p1 ||  ffmpeg -loglevel panic -nostdin -i $mp4 -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontcolor=white:fontsize=10:text='$s1'" -vframes 1 $p1 && echo -n . && updates=1
  test -f $p2 ||  ffmpeg -loglevel panic -nostdin -i $mp4 -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontcolor=white:fontsize=10:text='$s2'" -ss 00:01:00 -vframes 1 $p2 && echo -n . && updates=1
done
echo
if [ $updates -eq 1 ]; then
  (ffmpeg -loglevel panic -nostdin -y -framerate 20 -pattern_type glob -i "$dname/*.png" -c:v libx264 \
    -r 20 -pix_fmt yuv420p $dname/tmp.mp4 \
    && mv $dname/tmp.mp4 $dname/quick.mp4  && echo $dname/quick.mp4 ) || rm $dname/tmp.mp4
fi
