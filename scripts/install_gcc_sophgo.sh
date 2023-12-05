# https://milkv.io/docs/pioneer/resources/gcc

git clone 

./configure --prefix=/home/janniss/riscv-toolchain --with-arch=rv64imafdxtheadvector_zfh_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadfmv_xtheadint_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync --with-abi=lp64d
# --with-tune=c920

# for libgcc _zvamo0p7_zvlsseg0p7 otherwise unknown prefixed ISA extension `zvamo'
# update binutils to rvv07-upstream branch for gdb and binutils
# git checkout 03bbc77
dnf install isl-devel

export PATH=/home/janniss/riscv-toolchain/bin:$PATH

# for gcc build 
export LD_LIBRARY_PATH=/lib64/lp64d

# export C_INCLUDE_PATH=/usr/include
# export CPLUS_INCLUDE_PATH=/usr/include
# export LD_LIBRARY_PATH=/lib64/lp64d


# Findings

# merge commit in gcc-13
# https://gcc.gnu.org/git/?p=gcc.git;a=commitdiff;h=8351535f20b52cf332791f60d2bf22a025833516
