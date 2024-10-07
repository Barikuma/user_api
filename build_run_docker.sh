#!/bin/bash

read -p "Enter name for image: " image_name

read -p "Path to Dockerfile: " dockerfile

sudo docker build -t $image_name $dockerfile

read -p "Create and Run container?(y/n): " create

if [ $create == "y" ]; then
	read -p "Enter name for container: " container_name
	read -p "Enter port number to map with container (Container uses port 8000): " port
	sudo docker run -d -p "$port":8000 --name "$container_name" $image_name
	echo "Container is running"
	suod docker ps | grep $container_name
else
	exit 0
fi

