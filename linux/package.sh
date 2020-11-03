version=`cat ../version`
rm -rf ./dist/xet下载器_${version} >/dev/null 2>&1

pyinstaller -w main.spec

mkdir ./xet下载器_${version}
mv ./dist/xet下载器 ./xet下载器_${version}

cp ../readme.pdf ./xet下载器_${version}
cp ../xiaoeknow.js ./xet下载器_${version}

tar -czf xet下载器_${version}.tar.gz xet下载器_${version}
mv xet下载器_${version} ./dist/
