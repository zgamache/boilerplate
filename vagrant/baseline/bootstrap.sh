#!/usr/bin/env bash

inst()
{
    yum install -y "$@"
}

install_tmux()
{
    inst libevent-devel ncurses-devel
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
}

install_docker()
{
    inst yum-utils device-mapper-persistent-data lvm2
    yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    inst docker-ce
    systemctl enable docker
    systemctl start docker
}

install_dotfiles()
{
    mkdir code
    git clone https://github.com/zgamache/dotfiles code/dotfiles
    cd code/dotfiles
    ./install
    cd -
}

do_privileged()
{
    yum update -y
    inst git vim wget
}

do_unprivileged()
{
    install_dotfiles
}

case "$(whoami)" in
    "root")
        do_privileged
        ;;
    "vagrant")
        do_unprivileged
        ;;
    *)
        echo "ERROR: unexpected user=$(whoami)"
        exit 1
esac
