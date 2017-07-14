[ -f shop.json ] && mv shop.json shop-old.json
[ -f result.json ] && mv result.json result-old.json
curl -s https://api.chrono.gg/shop > shop.json
jq '.[] | select(.sold_out? != true) | { status: .status, name: .name?, price: .price, url: .url, platforms: .platforms }' shop.json > result.json
echo "< Old | New >" > diff.txt
diff result{-old,}.json >> diff.txt || pb push -t "Chrono Shop Update" -u https://chrono.gg/shop < diff.txt

