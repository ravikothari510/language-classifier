#!/bin/bash

# Download and uncompress the (1.5GB) eurpoar1.tgz data (takes 10 min)
mkdir -p downloaded
target=downloaded

if [ ! -f "${target}"/europarl.tgz ]; then
    wget http://www.statmt.org/europarl/v7/europarl.tgz -O "${target}"/europarl.tgz
fi

FOLDER=txt
if [ ! -d "${FOLDER}" ]; then
    tar xzf "${target}"/europarl.tgz
fi

# merge the individual text files into a large file (corpus) for each
# language (to free space, remove them after merge)
for i in $(ls txt); do
    find txt/$i -name "*.txt" -print0 | xargs -0 cat > txt/$i.txt
    rm -rf txt/$i
done
