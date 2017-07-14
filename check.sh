CACHE_DIR=cache

function notify {
  [ -d _env ] || virtualenv _env
  . _env/bin/activate
  pip install -r requirements.txt
  pb push -t "Chrono Shop Update" -u https://chrono.gg/shop < $CACHE_DIR/diff.txt
}

[ -d $CACHE_DIR ] || mkdir $CACHE_DIR

[ -f $CACHE_DIR/shop.json ] && mv $CACHE_DIR/shop.json $CACHE_DIR/shop-old.json
[ -f $CACHE_DIR/result.json ] && mv $CACHE_DIR/result.json $CACHE_DIR/result-old.json
curl -s https://api.chrono.gg/shop > $CACHE_DIR/shop.json
jq '.[] | select(.sold_out? != true) | { status: .status, name: .name?, price: .price, url: .url, platforms: .platforms }' $CACHE_DIR/shop.json > $CACHE_DIR/result.json
echo "< Old | New >" > $CACHE_DIR/diff.txt
diff $CACHE_DIR/result{-old,}.json >> $CACHE_DIR/diff.txt || notify

