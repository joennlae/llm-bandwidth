
mkdir -p install/bandwidth
cd install/bandwidth

wget https://zsmith.co/archives/bandwidth-1.12.5.tar.bz2
tar -xf bandwidth-1.12.5.tar.bz2

# nasm
wget https://www.nasm.us/pub/nasm/releasebuilds/2.16.01/nasm-2.16.01.tar.gz
tar -xf nasm-2.16.01.tar.gz

# install nasm
cd nasm-2.16.01
./configure
make -j 8

export PATH="$PATH:$PWD"

cd ..

# install bandwidth
cd bandwidth-1.12.5
make