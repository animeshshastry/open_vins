build:
	docker build -f Dockerfile_ros2_22_04 . -t openvins --rm

cpu_run:
	docker run -itd --rm --ipc host --net host --pid host --name openvins openvins

# gpu_run:
# 	docker run -itd --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --gpus all -v /dev:/dev -e NVIDIA_DRIVER_CAPABILITIES=all --rm --ipc host --net host --pid host --name openvins openvins

gpu_run:
	docker run -itd --rm --net=host --pid host --ipc host --gpus all \
    --env=\"NVIDIA_DRIVER_CAPABILITIES=all\" --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
	-v /dev:/dev \
	-v /home/animesh/workspaces/ros2_ws_ov:/home/ros2_ws \
	--name openvins openvins

start:
	docker start openvins

stop:
	docker stop openvins

kill:
	docker kill openvins

attach:
	docker exec -it openvins bash

commit:
	docker commit openvins openvins2
	docker kill openvins
	docker tag openvins2 openvins
