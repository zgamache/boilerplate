echo "Updating and installing packages"
yum update -y
yum install -y git vim wget

# tmux
echo "Installing tmux"
yum install -y libevent-devel ncurses-devel
wget https://github.com/tmux/tmux/releases/latest
version="`grep Release.*tmux latest | sed -n 's/.*\([0-9]\+\.[0-9]\+\).*/\1/p'`"
path="tmux-${version}"
archive="${path}.tar.gz"
wget wget https://github.com/tmux/tmux/releases/download/${version}/${archive}
tar -xzf $archive
cd $path
./configure
make install
cd -
rm -rf $archive $path latest

# docker
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install -y docker-ce
systemctl enable docker
systemctl start docker
