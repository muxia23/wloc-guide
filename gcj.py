#!/usr/bin/env python3
"""GCJ-02 → WGS-84 坐标转换。

Apple 地图 / 高德在中国大陆分享出来的链接里是 GCJ-02（火星坐标），
而 wloc 的储存接口要的是 WGS-84，两者在国内相差 300~800 米。

用法:
    python3 gcj.py 39.908722 116.397496     # 直接给 纬度 经度
    python3 gcj.py 'https://maps.apple.com/place?...&coordinate=39.908722,116.397496&...'

算法镜像自 wloc 仓库的 worker/src/gcj-browser.js，输出与其 /api/parse 逐位一致。
"""
import math
import re
import sys

A = 6378245.0
EE = 0.00669342162296594323


def out_of_china(lng, lat):
    return lng < 72.004 or lng > 137.8347 or lat < 0.8293 or lat > 55.8271


def _dlat(x, y):
    r = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    r += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    r += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
    r += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
    return r


def _dlon(x, y):
    r = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    r += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    r += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
    r += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0
    return r


def wgs2gcj(lat, lon):
    if out_of_china(lon, lat):
        return lat, lon
    d_lat = _dlat(lon - 105.0, lat - 35.0)
    d_lon = _dlon(lon - 105.0, lat - 35.0)
    rad = lat / 180.0 * math.pi
    magic = 1 - EE * math.sin(rad) ** 2
    sq = math.sqrt(magic)
    d_lat = (d_lat * 180.0) / ((A * (1 - EE)) / (magic * sq) * math.pi)
    d_lon = (d_lon * 180.0) / ((A / sq) * math.cos(rad) * math.pi)
    return lat + d_lat, lon + d_lon


def gcj2wgs(lat, lon):
    """牛顿迭代反解。GCJ-02 加偏是不可逆的闭源算法，只能这样逼近。"""
    if out_of_china(lon, lat):
        return lat, lon
    w_lat, w_lon = lat, lon
    for _ in range(6):
        g_lat, g_lon = wgs2gcj(w_lat, w_lon)
        e_lat, e_lon = g_lat - lat, g_lon - lon
        if abs(e_lat) < 1e-9 and abs(e_lon) < 1e-9:
            break
        w_lat -= e_lat
        w_lon -= e_lon
    return w_lat, w_lon


def extract(text):
    """从地图链接或纯文本里抠出 纬度,经度。"""
    m = re.search(r"(?:coordinate|ll|sll|q)=(-?\d{1,3}\.\d+)(?:,|%2C)(-?\d{1,3}\.\d+)", text, re.I)
    if not m:
        m = re.search(r"(-?\d{1,3}\.\d{4,})\s*,\s*(-?\d{1,3}\.\d{4,})", text)
    if not m:
        return None
    return float(m.group(1)), float(m.group(2))


def main():
    args = sys.argv[1:]
    if len(args) == 2:
        lat, lon = float(args[0]), float(args[1])
    elif len(args) == 1:
        got = extract(args[0])
        if not got:
            sys.exit("没能从输入里找到坐标。直接给两个数字试试：python3 gcj.py 纬度 经度")
        lat, lon = got
    else:
        sys.exit(__doc__)

    w_lat, w_lon = gcj2wgs(lat, lon)
    dy = (w_lat - lat) * 111320
    dx = (w_lon - lon) * 111320 * math.cos(math.radians(lat))

    print(f"GCJ-02 (地图链接里的): {lat}, {lon}")
    print(f"WGS-84 (填进 wloc 的): {w_lat:.6f}, {w_lon:.6f}")
    print(f"两者相差 {math.hypot(dx, dy):.0f} 米")
    print()
    print("https://gs-loc.apple.com/wloc-settings/save"
          f"?lat={w_lat:.6f}&lon={w_lon:.6f}&acc=25")


if __name__ == "__main__":
    main()
