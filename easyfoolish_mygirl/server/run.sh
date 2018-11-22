
if [ -f /etc/redhat-release ]; then
	echo "redhat"

fi 

if [ -f /etc/lsb-release ]; then

	echo "ubuntu"
fi



cd deep_painterly && \
nohup  th daemon_gram.lua >>a1.log&& \
nohup  th daemon_paint.lua >>a1.log&& \
nohup  python daemon.py >>a1.log&& \
cd ../ && \
\
\
\
\
cd detectron && \
nohup  python daemon.py >>a1.log&& \
cd ../ && \
\
\
\
cd portrait_seg_tf && \
nohup  python daemon.py >>a1.log&& \
cd ../ 