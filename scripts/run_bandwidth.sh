mkdir -p results/bandwidth
# ./install/bandwidth/bandwidth-1.13.2/bandwidth64 --unlimited --nosse2 --nosse4 --noavx --noregister --csv results/bandwidth/output.csv --nice | tee results/bandwidth/output.txt

./install/bandwidth/bandwidth-1.13.2/bandwidth64 --fast --noregister --csv results/bandwidth/output.csv --nice | tee results/bandwidth/output.txt