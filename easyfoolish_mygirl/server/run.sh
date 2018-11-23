
if [ -f /etc/redhat-release ]; then
	echo "redhat"

fi 

if [ -f /etc/lsb-release ]; then

	echo "ubuntu"
fi

export PATH="/$HOME/anaconda2/envs/caffe2_conda/bin:$PATH"
python -c 'from caffe2.python import core' 2>/dev/null && echo "Success" || echo "Failure"



export PYTHONPATH=$PYTHONPATH:$(pwd)"/../../"
python -c 'from easyfoolish_mygirl.common import caffe2_pb2' 2>/dev/null && echo "easyfoolish_mygirl Success" || echo "easyfoolish_mygirl Failure"




cd deep_painterly 
CUDA_VISIBLE_DEVICES=0 nohup  python daemon_gram.py >a1.log&
CUDA_VISIBLE_DEVICES=0 nohup  python daemon_paint.py >a2.log&
nohup    python daemon.py  2>&1 >a3.log &
cd ../ 


echo `pwd`

cd detectron 
CUDA_VISIBLE_DEVICES=0 nohup python  daemon.py >a1.log  &
cd ../ 


echo `pwd`

cd portrait_seg_tf 
CUDA_VISIBLE_DEVICES=3 nohup python daemon.py >a1.log &
cd ../ 



echo "finish...."
