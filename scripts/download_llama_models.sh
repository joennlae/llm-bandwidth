
# Download the llama 2 7b models
mkdir -p models
cd models

# conda install -c conda-forge git-lfs -y
git lfs install

git lfs clone https://huggingface.co/TheBloke/Llama-2-7B-GGUF
cd ..
