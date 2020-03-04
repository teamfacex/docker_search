
# FaceX Docker SDK 

## 📑 Index
* [Getting Started](#getting-started)
   * [Prerequisites](#prerequisites)
   * [Installing](#installing)   
          * [Ubuntu](#ubuntu)
            * [Arch Linux](#arch-linux)    
* [Getting The SDK](#getting-the-sdk)
   * [server_video](#server_video)
   * [server_search](#server_search)
   * [data-wrangler](#data-wrangler)
* [Customization](#customization)
   * [Fine Tune the docker-compose.yml](#fine-tune-the-docker-composeyml)
          * [Optional-Setup NVIDIA & CUDA](#optional-setup-nvidia---cuda)
                * [Ubuntu](#ubuntu-1)
* [Website](#website)


## Getting Started
These instructions will help you setup FaceX docker instance on your linux system.

### Prerequisites
Docker CE
Docker-Compose

```
Tested Distributions:-
Ubuntu 
Debian
Arch Linux

Docker version:-
Docker CE 19+
docker-compose 1.2+
```

### Installing 
#### Ubuntu 
Follow these steps to get Docker installed on your system

```
sudo apt remove docker docker-engine docker.io
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install docker-ce
sudo usermod -aG docker $USER
newgrp docker
```
Note if any issue with fingerprint or key, add the missing key to  keyserver

Now install docker-compose

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

docker-compose --version
```

### Arch Linux

```
sudo pacman -S docker
sudo usermod -aG docker $USER
newgrp docker
sudo systemctl start docker.service
```

This will setup a running docker service .

Now install docker-compose

```
sudo pacman -S docker-compose

docker-compose --version
```

## Getting The SDK

##### Download docker images
Download the docker images from the link provided.Three docker images are available, each with a specific use case.

* server_search.tar 
 to create a searchable database of images with apis to search for images.

* server_video.tar
 to be used in combination with server_search image to detect faces from video feed and perform search

##### Load the docker image
 Based on requirement load one or multiple docker images to your system after downloading the image, using following command
 
 ```
docker image load -i

eg:-
docker image load -i server_search.tar
docker image load -i server_video.tar
```
##### Clone this github repositoy

```
git clone https://github.com/teamfacex/docker_search.git
```

change directory to search or video+search based on your requirement.

```
cd docker-sdk/search
cd docker-sdk/video+search
```
##### License
If you are a new customer looking for credentials, please email us at team@facex.io
Edit USER environment variable in [docker-compose.yml](). 

```
environment:
 -USER=xxxx  => 
environment:
 -USER=your_user_id
```
Then execute bash script runDocker

```
bash runDocker.sh
```
This will spinup the required docker instance.

* data-wrangler server 
* server_video
* server_search



###### server_video

 ```
This is the instance that detect the faces appearing on the video feed

Default video device is  /dev/video0

Detected faces will be saved under images directory in ($PWD) as png files

Whenever the faces are detected, the detected faces will be sent to server_search for identification
```

###### server_search

This instance exposes following apis

* add_user - http://0.0.0.0:5000/add_user

* delete_user - http://0.0.0.0:5000/delete_user

* add_user_bulk - http://0.0.0.0:5000/add_user_bulk

* search_user - http://0.0.0.0:5000/search_user

* find_user - http://0.0.0.0:5000/find_user

* get_count - http://0.0.0.0:5000/get_count

* init - http://0.0.0.0:5000/init



* add_user 

```
request type: POST
url: http://0.0.0.0:5000/add_user || http://0.0.0.0:5000/add_user?det=1

body-form-fields:-

img:face_image_file
name:name_of_user

use: to save a face for future searching.

note: 
    -data stored in $PWD/data/data.db
    -if name is not unique it will overwrite existing data.
    -param det=1 will find and crop the first detected face in the input image
```

* delete_user

```
request type: POST
url: http://0.0.0.0:5000/delete_user 

body-form-fields:-

name:name_of_user

use: to delete set of images stored under a single users name.

note: 
    -data stored in $PWD/data/data.db
    -if name is not unique it will overwrite existing data.
```

* add_user_bulk

```
request type: GET
url: http://0.0.0.0:5000/add_user_bulk

use: to save a multiple face for future searching.

note: 
    -faces in images should be tightly cropped
    -images should be stored in $PWD/bulk
    -images to be stored should be uniquely named as per the person's name it belongs to
    -if name is not unique it will overwrite thte existing data
    -every file in the directory must be an image file
    -data is stored in $PWD/data/data.db
    -when processing is done each image will be removed from the directory
```

* search_user

```
request type: POST
url: http://0.0.0.0:5000/search_user || http://0.0.0.0:5000/search_user?det=1

body-form-fields:-

img:face_image_file

use: to search for user in the users db.
note: 
    -make sure there is an existing user database - $PWD/data/data.json
    -it will return a dict of users sorted by vector distance. 
    -user with least distance will be the most probable macth.
    -param det=1 will find and crop the first identified face in the input image
```

* find_user

```
request type: POST
url: http://0.0.0.0:5000/find_user || http://0.0.0.0:5000/find_user?det=1

body-form-fields:-

img:face_image_file

use: to search for user in the users db. 
note: 
    -it will not return the users is directly instead calls the wrangler-server with users list.
    -make sure there is an existing user database - $PWD/data/data.json
    -this will also save a log of the users dict in $PWD/log/detect.txt
    -param det=1 will find and crop the first identified face in the input image
```

* init 

```
request type: GET
url: http://0.0.0.0:5000/init

use: to  initialise the search object after adding images to database. Searching for newly added images will only work after this get request is called.
```

* get_count

```
request type: GET
url: http://0.0.0.0:5000/get_count

use: to  get the total number of users and images stored in database.
```


###### data-wrangler

A fully customizable flask server which gets called when faces are detected. This can be customized according to users need to start a service or call an api with identified names. It will return {} if no match is found.

```
In its current form it just saves the probable matches in $PWD/wrangler/data.txt

The code for the server is availbale in the data-wrangler directory in the cloned repo.
```


## Customization
### Fine Tune the [docker-compose.yml]()

Params

1)  device & URL


```
#default setting
devices:
 -/dev/video0:/dev/video0
environment:
 -URL=0

#eg change:
devices:
 -/dev/video1:/dev/video0
environment:
 -URL=0

#or:
devices:
 -/dev/video1:/dev/video0
environment:
 -URL=0
```

2)  USER

```
#default setting:
environment:
 -USER=your_user_id
change this to user id given in the email
```


#### Optional-Setup NVIDIA  & CUDA  
##### Ubuntu
Making GPUs accessible in Docker Instance, for GPU accelerated docker instances.

```
# Add the package repositories
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

###########################TESTING###########################
#Optional
#Testing GPUs are accessible
docker run --gpus all nvidia/cuda:9.0-base nvidia-smi
#Testing if CUDA is working
nvidia-docker run  --rm nvidia/cuda nvcc  -V

#############################################################
```

to the startup script add following arguments in runDocker

```
--gpus all
```

to get CUDA mounted, add following to docker run in runDocker

```
-v /usr/local/cuda:/usr/local/cuda
```

## Website 

* **FaceX**  - [facex](https://facex.io)