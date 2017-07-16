#!/bin/bash -x

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export CACHE_DIR=$DIR/cache

function notify {
  (
    echo "< Old | New >"
    cat $CACHE_DIR/diff.txt
  ) > $CACHE_DIR/message.txt
  cat $CACHE_DIR/message.txt
  cat $CACHE_DIR/message.txt | pb push -t "Chrono Shop Update" -u https://chrono.gg/shop 
}

[ -d _env ] || virtualenv _env
. _env/bin/activate
pip install -r requirements.txt

[ -d $CACHE_DIR ] || mkdir $CACHE_DIR

[ -f $CACHE_DIR/shop.json ] && mv $CACHE_DIR/shop.json $CACHE_DIR/shop-old.json
[ -f $CACHE_DIR/result.json ] && mv $CACHE_DIR/result.json $CACHE_DIR/result-old.json
curl -s https://api.chrono.gg/shop > $CACHE_DIR/shop.json
jq '[.[] | select(.sold_out? != true) | { status: .status, name: .name?, price: .price, url: .url, platforms: .platforms }]' $CACHE_DIR/shop.json > $CACHE_DIR/result.json
python check.py > $CACHE_DIR/diff.txt || notify

