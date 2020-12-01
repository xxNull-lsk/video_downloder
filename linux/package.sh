version=`cat ../.version`
rm -rf ./dist/video_downloader_${version} >/dev/null 2>&1

pyinstaller -w main.spec

mkdir ./video_downloader_${version}
mv ./dist/video_downloader ./video_downloader_${version}

cp ../readme.pdf ./video_downloader_${version}
cp "../video downloader.js" ./video_downloader_${version}

tar -czf linux_video_downloader_${version}.tar.gz video_downloader_${version}
mv video_downloader_${version} ./dist/
