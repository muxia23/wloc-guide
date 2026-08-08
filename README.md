> 本项目基于 https://github.com/Yu9191/wloc

# 教程
## Step1
确保手机有如下某一个软件**Surge**、**Quantumult X**、**Loon**、**Stash**、**Shadowrocket**  
接下来以 **Shadowrocket** 为例  
点选进入配置  
![a1b772f4cfa01ae32af5e4dc1384c41f.jpg](https://pic.m2xal3u.top/PicGo_Library/a1b772f4cfa01ae32af5e4dc1384c41f.jpg)  
复制对应的url
- **Surge:** [https://raw.githubusercontent.com/Yu9191/wloc/refs/heads/main/modules/wloc.sgmodule](https://raw.githubusercontent.com/Yu9191/wloc/refs/heads/main/modules/wloc.sgmodule)
- **Quantumult X:** [https://raw.githubusercontent.com/Yu9191/wloc/refs/heads/main/modules/wloc.conf](https://raw.githubusercontent.com/Yu9191/wloc/refs/heads/main/modules/wloc.conf)
- **Loon:** [https://raw.githubusercontent.com/Yu9191/wloc/refs/heads/main/modules/wloc.lpx](https://raw.githubusercontent.com/Yu9191/wloc/refs/heads/main/modules/wloc.lpx)
- **Stash:** [https://raw.githubusercontent.com/Yu9191/wloc/refs/heads/main/modules/wloc.stoverride](https://raw.githubusercontent.com/Yu9191/wloc/refs/heads/main/modules/wloc.stoverride)
- **Shadowrocket:** [https://raw.githubusercontent.com/Yu9191/wloc/refs/heads/main/modules/wloc.module](https://raw.githubusercontent.com/Yu9191/wloc/refs/heads/main/modules/wloc.module)  
![c890eafeede149ed538a56d5df96b009.png](https://pic.m2xal3u.top/PicGo_Library/c890eafeede149ed538a56d5df96b009.png)  
接着点击你的配置文件，找到HTTPS解密，打开解密功能，生成一个新的CA证书，安装证书，接着在设置中进入已下载描述文件，按提示安装，最后在关于本机页面底部，信任证书设置即可  
这部分可参考[此视频](https://b23.tv/94WVoOw)

## Step2
接着在快捷指令app中导入这两个快捷指令即可
- **wloc 设置地理位置**：[https://www.icloud.com/shortcuts/a82717d8fdad4e6280866fcf911173f7](https://www.icloud.com/shortcuts/a82717d8fdad4e6280866fcf911173f7)
- **wloc 清理恢复位置**：[https://www.icloud.com/shortcuts/f42632d406504f24a2cd163af4fe012f](https://www.icloud.com/shortcuts/f42632d406504f24a2cd163af4fe012f)

到这里就能用了：打开选点页面选位置 → 储存到设备。

# 进阶：一键切到固定地址

上面那个「设置地理位置」每次都要开选点页面点一下。如果你有天天要切的固定地点（宿舍、家、公司），
可以做一个一键切换的快捷指令，点一下就好，不用开网页。

## 原理

选点页面做的事情其实只有一件——往下面这个地址发一个 GET 请求，被代理模块拦截后写进本地储存：

```
https://gs-loc.apple.com/wloc-settings/save?lat=<纬度>&lon=<经度>&acc=25
```

所以固定地址的快捷指令只需要**两个动作**：

1. 「获取 URL 内容」→ 粘贴上面那条 URL（方法保持默认 GET）
2. 「显示通知」→ 正文里插入变量「获取 URL 内容的结果」

第 2 步别省。模块正常工作时通知会显示 `{"success":true,...}`；要是模块没启用或 MITM 掉了，
请求会真的打到 Apple 服务器返回 404，你从通知内容一眼就能分辨，省得定位没变还以为是坐标填错了。

其他可用参数：

| 参数 | 说明 |
| --- | --- |
| `acc` | 上报的定位精度（米），默认 25。调小（如 `acc=10`）系统更倾向采信这个网络定位 |
| `randomRadius` | 每次响应在目标点周围随机抖动的最大半径（米），默认 0 关闭 |
| `?action=clear` | 清除已储存坐标，恢复真实定位 |
| `?action=query` | 查询当前储存了什么坐标，排查用 |

## ⚠️ 坐标系：最容易踩的坑

**wloc 接口要的是 WGS-84，而 Apple 地图和高德在中国大陆分享出来的链接里是 GCJ-02（火星坐标）。**
直接把链接里的数字抄进去，定位会偏 300~800 米。

本仓库的 `gcj.py` 负责这个转换，把地图链接或坐标丢给它就行：

```bash
python3 gcj.py 39.908722 116.397496
# 或者直接把整条地图链接用引号包起来丢进去
python3 gcj.py 'https://maps.apple.com/place?...&coordinate=39.908722,116.397496&...'
```

输出：

```
GCJ-02 (地图链接里的): 39.908722, 116.397496
WGS-84 (填进 wloc 的): 39.907321, 116.391255
两者相差 555 米

https://gs-loc.apple.com/wloc-settings/save?lat=39.907321&lon=116.391255&acc=25
```

最后那行直接复制进「获取 URL 内容」就完事了。

## 批量生成（可选）

如果地点比较多、懒得一个个手搓，`build_shortcuts.py` 可以直接生成签好名的 `.shortcut` 文件
（macOS 专用，用到了系统自带的 `shortcuts sign`）：

```bash
cp places.example.json places.json   # 改成你自己的地点，坐标填 WGS-84
python3 build_shortcuts.py           # 产物在 signed/
```

生成的文件 AirDrop 到 iPhone 点开就能导入。除了你配置的地点，还会附带
「恢复真实定位」和「查看当前定位」两个。

> `places.json` 已在 `.gitignore` 里——你的常用地址不会被提交上去。
>
> 顺带一提：**分享到 iCloud 的快捷指令，任何人在导入前的预览界面就能看到里面的坐标。**
> 如果你做的是「回宿舍」这种，别把 iCloud 链接公开发出去。

# WARNING
原作者提示：iOS26、27可能有location的缓存，导致无法成功替换，可用下面两个方法  
**高版本系统推荐操作流程（成功率最高）：**

方法一：
1. 先在选点页面选好需要修改的定位并储存到设备
2. 开飞行模式 → 关闭定位服务 → 重启设备
3. 关闭飞行模式（WiFi 也要关）→ 连接代理工具（确认 VPN 图标出现）→ 打开定位服务
4. 打开地图验证

方法二：
1. 关闭定位服务
2. 在选点页面选好位置并储存到设备
3. 打开定位服务 → 弹出「允许访问位置信息」时选择**「下次询问或在我共享时」**
4. 打开地图验证

- 仅修改网络定位(WiFi/基站)，不影响 GPS 硬件定位
- iOS 在 GPS 信号强时可能忽略网络定位结果
- 适用于 WiFi 定位为主的室内场景效果最佳
