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
接着在快捷指令app中导入这三个快捷指令即可
- **wloc 设置地理位置**：[https://www.icloud.com/shortcuts/a82717d8fdad4e6280866fcf911173f7](https://www.icloud.com/shortcuts/a82717d8fdad4e6280866fcf911173f7)
- **wloc 清理恢复位置**：[https://www.icloud.com/shortcuts/f42632d406504f24a2cd163af4fe012f](https://www.icloud.com/shortcuts/f42632d406504f24a2cd163af4fe012f)
- **回宿舍（注：此快捷指令为固定地址，可获取常用地址的WGS-84地址替换，不懂的可以问ai）**：[https://www.icloud.com/shortcuts/7cac6a1f8b9240ab8486bf8987340c9d](https://www.icloud.com/shortcuts/7cac6a1f8b9240ab8486bf8987340c9d)

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
