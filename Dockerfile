from ubuntu

maintainer Sidali HALLAK, sidali@iogrow.com

#ENV http_proxy http://10.0.0.1:80
#ENV https_proxy http://10.0.0.1:80


run apt-get update
run apt-get install -y build-essential git
run apt-get install -y python python-dev python-setuptools python-pip
run apt-get install -y nginx supervisor


# install uwsgi now because it takes a little while
run pip install uwsgi

# install nginx
run apt-get install -y software-properties-common python-software-properties
run apt-get update
run apt-get install -y sqlite3
run apt-get install -y wget
## install neo4j according to http://www.neo4j.org/download/linux
# Import neo4j signing key
# Create an apt sources.list file
# Find out about the files in neo4j repo ; install neo4j community edition

run wget -O - http://debian.neo4j.org/neotechnology.gpg.key | apt-key add - && \
    echo 'deb http://debian.neo4j.org/repo stable/' > /etc/apt/sources.list.d/neo4j.list && \
    apt-get update ; apt-get install neo4j -y


# install our code
add . /home/docker/code/

# setup all the configfiles
run echo "daemon off;" >> /etc/nginx/nginx.conf
run rm /etc/nginx/sites-enabled/default
run ln -s /home/docker/code/nginx-app.conf /etc/nginx/sites-enabled/
run ln -s /home/docker/code/supervisor-app.conf /etc/supervisor/conf.d/

## add launcher and set execute property
## clean sources
## turn on indexing: http://chrislarson.me/blog/install-neo4j-graph-database-ubuntu
## enable neo4j indexing, and set indexable keys to name,age
# enable shell server on all network interfaces

add launch.sh /
run chmod +x /launch.sh && \
    apt-get clean && \
    sed -i "s|#node_auto_indexing|node_auto_indexing|g" /var/lib/neo4j/conf/neo4j.properties && \
    sed -i "s|#node_keys_indexable|node_keys_indexable|g" /var/lib/neo4j/conf/neo4j.properties && \ 
    echo "remote_shell_host=0.0.0.0" >> /var/lib/neo4j/conf/neo4j.properties

# run pip install
run pip install -r /home/docker/code/app/requirements.txt


expose 80
expose 7474
expose 1337



## entrypoint
cmd ["supervisord", "-n"]
