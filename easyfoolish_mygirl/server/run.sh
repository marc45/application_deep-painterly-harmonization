
if [ -f /etc/redhat-release ]; then
	echo "redhat"

fi 

if [ -f /etc/lsb-release ]; then

	echo "ubuntu"
fi



cd deep_painterly 
CUDA_VISIBLE_DEVICES=0 nohup  th daemon_gram.lua >a1.log&
CUDA_VISIBLE_DEVICES=0 nohup  th daemon_paint.lua >a2.log&
nohup    python daemon.py  2>&1 >a3.log &
cd ../ 


echo `pwd`

cd detectron 
CUDA_VISIBLE_DEVICES=0 nohup  python  daemon.py >a1.log  &
cd ../ 


echo `pwd`

cd portrait_seg_tf 
CUDA_VISIBLE_DEVICES=3 nohup  python daemon.py >a1.log &
cd ../ 



echo "finish...."
