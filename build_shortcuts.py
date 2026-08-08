#!/usr/bin/env python3
"""生成并签名 wloc 定位切换快捷指令。

地点读自 places.json（复制 places.example.json 改），坐标必须是 WGS-84 ——
地图链接里的是 GCJ-02，先用 gcj.py 转换。

    python3 build_shortcuts.py

产物在 signed/，AirDrop 到 iPhone 直接导入。
"""
import json
import plistlib
import subprocess
import sys
import uuid
from pathlib import Path

OUT = Path(__file__).parent
ENDPOINT = "https://gs-loc.apple.com/wloc-settings/save"
OBJ = "￼"  # Shortcuts 用来占位变量的 OBJECT REPLACEMENT CHARACTER


def text(string, attachments=None):
    """WFTextTokenString: attachments 按 OBJ 在字符串里出现的顺序依次配对。"""
    by_range = {}
    if attachments:
        positions = [i for i, c in enumerate(string) if c == OBJ]
        for pos, att in zip(positions, attachments):
            by_range["{%d, 1}" % pos] = att
    return {
        "WFSerializationType": "WFTextTokenString",
        "Value": {"string": string, "attachmentsByRange": by_range},
    }


def action(ident, params):
    return {"WFWorkflowActionIdentifier": ident, "WFWorkflowActionParameters": params}


def build(url, body_prefix, color):
    result_uuid = str(uuid.uuid4())
    actions = [
        action("is.workflow.actions.downloadurl", {
            "UUID": result_uuid,
            "CustomOutputName": "Result",
            "WFHTTPMethod": "GET",
            "WFURL": text(url),
        }),
        # 把接口返回的 JSON 原样弹出来: 模块正常时是 {"success":true,...};
        # 模块没开的话请求会真的打到 Apple 服务器返回 404, 一眼能分辨。
        action("is.workflow.actions.notification", {
            "UUID": str(uuid.uuid4()),
            "WFNotificationActionTitle": "WLOC",
            "WFNotificationActionBody": text(
                body_prefix + OBJ,
                [{"Type": "ActionOutput", "OutputName": "Result", "OutputUUID": result_uuid}],
            ),
        }),
    ]
    return {
        "WFWorkflowMinimumClientVersionString": "900",
        "WFWorkflowMinimumClientVersion": 900,
        "WFWorkflowClientVersion": "5028.0.21",
        "WFWorkflowIcon": {
            "WFWorkflowIconStartColor": color,
            "WFWorkflowIconGlyphNumber": 61444,
        },
        "WFWorkflowActions": actions,
        "WFWorkflowInputContentItemClasses": [],
        "WFWorkflowOutputContentItemClasses": [],
        "WFWorkflowImportQuestions": [],
        "WFWorkflowTypes": ["WFWorkflowTypeShowInSearch"],
        "WFQuickActionSurfaces": [],
        "WFWorkflowHasShortcutInputVariables": False,
        "WFWorkflowHasOutputFallback": False,
    }


BLUE, RED, YELLOW = 463140863, 4282601983, 4271458815


def load_places():
    cfg = OUT / "places.json"
    if not cfg.exists():
        sys.exit("缺少 places.json —— 先 cp places.example.json places.json 再改成你的地点。")
    data = json.loads(cfg.read_text(encoding="utf-8"))
    jobs = []
    for p in data["places"]:
        url = f"{ENDPOINT}?lat={p['lat']}&lon={p['lon']}&acc={p.get('acc', 25)}"
        if p.get("randomRadius"):
            url += f"&randomRadius={p['randomRadius']}"
        body = f"{p.get('note', p['name'])}\n{p['lat']}, {p['lon']}\n"
        jobs.append((f"{p['name']}.shortcut", url, body, BLUE))
    jobs.append(("恢复真实定位.shortcut", f"{ENDPOINT}?action=clear", "已清除虚拟定位\n", RED))
    jobs.append(("查看当前定位.shortcut", f"{ENDPOINT}?action=query", "当前储存的坐标\n", YELLOW))
    return jobs


def main():
    # 未签名的 .shortcut 在 iOS 上会被拒绝导入。macOS 自带的 shortcuts 命令能签,
    # 签完是 AEA1 容器, AirDrop 过去直接能开, 不用碰「允许不受信任的快捷指令」开关。
    unsigned, signed = OUT / "unsigned", OUT / "signed"
    unsigned.mkdir(exist_ok=True)
    signed.mkdir(exist_ok=True)

    for name, url, body, color in load_places():
        raw = unsigned / name
        with open(raw, "wb") as f:
            plistlib.dump(build(url, body, color), f, fmt=plistlib.FMT_BINARY)
        out = signed / name
        subprocess.run(
            ["shortcuts", "sign", "--mode", "anyone", "--input", str(raw), "--output", str(out)],
            check=True,
        )
        print(f"{out}  ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
