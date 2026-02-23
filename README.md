**⚠️ 免责声明：本版本在原版基础上进行过修改。**

# Bili23-Downloader-ColdFix

<p align="center">
    <a href="https://bili23.scott-sloan.cn" target="_blank">
        <img src="https://bili23.scott-sloan.cn/logo.png" alt="Bili23 Downloader" style="width: 500px;"/>
    </a>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/GitHub-black?logo=github&style=flat-square" alt="GitHub"/>
    <img src="https://img.shields.io/badge/Platform-Windows_|_Linux_|_macOS-blue?style=flat-square" alt="Platform"/>
    <img src="https://img.shields.io/badge/license-MIT-orange?style=flat-square" alt="License"/>
    <img src="https://img.shields.io/badge/ARIA2-支持-brightgreen?style=flat-square" alt="ARIA2"/>
</p>

<p align="center">
    <img src="https://img.shields.io/github/v/release/ScottSloan/Bili23-Downloader?style=flat-square" alt="Version"/>
    <img src="https://img.shields.io/badge/Python-3.12.10-green?style=flat-square" alt="Python"/>
    <img src="https://img.shields.io/badge/wxPython-4.2.4-green?style=flat-square" alt="wxPython"/>
</p>

<p align="center">
    <a href="https://bili23.scott-sloan.cn/" target="_blank">项目官网</a>
</p>

<p align="center">
    Bili23 Downloader 是一款跨平台（Windows/Linux/macOS）的 B 站视频下载工具，支持下载 B 站投稿视频、番剧、电影等类型视频。支持多线程加速、断点续传等特性，搭配图形化界面与零配置操作，提供高效便捷的下载体验。
</p>

<p align="center">
    <b>🔥 Coldfix 修改版新增 ARIA2 多线程下载支持，下载速度大幅提升！</b>
</p>

## 🆕 Coldfix 修改版特性

本版本在原版基础上进行了以下增强：

### ARIA2 多线程下载

- ✅ **本地模式**：自动启动内置 ARIA2 进程，开箱即用
- ✅ **RPC 模式**：连接外部 ARIA2 服务（如 AriaNg、WebUI）
- ✅ **自动检测**：自动检测环境变量和运行目录中的 ARIA2
- ✅ **多线程加速**：可配置线程数（默认 16 线程），显著提升下载速度
- ✅ **断点续传**：支持下载中断后恢复，大文件更稳定
- ✅ **速度限制**：支持设置下载速度上限
- ✅ **代理支持**：自动继承程序的代理设置
- ✅ **智能回退**：ARIA2 失败时自动回退到原生下载

### 便携化改进

- ✅ **绿色便携**：配置存储改为程序目录下的 `data` 文件夹
- ✅ **即拷即用**：程序文件夹可直接复制移动，配置不丢失
- ✅ **路径修复**：自动检测并修复无效的配置路径

### 打包工具

- ✅ **build.py**：PyInstaller 打包脚本，支持 UPX 压缩
- ✅ **clean.py**：清理构建文件的辅助脚本

## 🌟 社区交流

加入社区，获取项目最新动态、问题答疑和技术交流。

* QQ 交流群
  
  * [主群](https://qm.qq.com/q/KX3uJIFIYK)

* QQ 频道
  
  * [频道](https://pd.qq.com/s/8941to1p0)

> 如需提问，请提供**问题描述**、**完整日志**，以便我们更好地提供帮助。
> 
> **注意**：本修改版相关问题请明确说明使用的是 Coldfix 版本。

## ⚡ 程序特性

* 跨平台（兼容 Windows、Linux、macOS 三大平台）
* GUI 图形化界面，零配置开箱即用，适配高分屏显示
* 支持解析UP主投稿视频、番剧、电影、课程等类型链接
* 支持自动识别短链接（b23.tv）、活动专题页（如拜年祭、二游新春会）链接
* 支持自定义下载视频分辨率、音质以及编码格式
* 支持下载 ASS 弹幕、字幕、封面、NFO 元数据
* 支持下载 Hi-Res 无损、杜比全景声音质
* 支持下载收藏夹、UP 个人主页投稿视频
* 支持完整下载互动视频所有分支，自动生成可视化剧情树
* 支持断点续传、下载限速、并行下载、自动重试等功能
* 支持视频格式转换、片段截取、音频提取等功能
* **🔥 支持 ARIA2 多线程下载，速度更快更稳定（Coldfix 新增）**

## 📄 使用说明

### ARIA2 配置说明

1. **本地模式（推荐）**
   
   - 将 `aria2c.exe` 放在程序同目录下，或确保其在系统 PATH 中
   - 在设置 -> ARIA2 中点击"自动检测"
   - 启用 ARIA2 下载即可

2. **RPC 模式**
   
   - 如果你有正在运行的 ARIA2 服务（如 AriaNg）
   - 在设置中填写 RPC 地址、端口和密钥
   - 点击"测试连接"验证配置

3. **线程数设置**
   
   - 默认 16 线程，可根据网络情况调整
   - 建议值：8-32 线程

有关本程序的更多使用说明，请参考[项目文档](https://bili23.scott-sloan.cn/doc/what-is-bili23-downloader.html)。

## 🪧 免责声明

本项目仅供个人学习与研究用途，任何通过本项目下载的内容仅限于个人使用，不得用于任何形式的商业目的、公开传播或分发。
用户需自行承担使用本项目可能带来的所有风险，项目开发者不对因使用本项目所引发的任何法律纠纷、版权问题或其他损害承担责任。

**关于本修改版**：

- 本版本（coldfix）为第三方修改版本，非官方原版
- 修改内容包括但不限于：集成 ARIA2 下载功能、便携化配置存储
- 使用本版本产生的任何问题，请自行承担风险
- 如遇问题建议先测试官方原版以排除修改引入的问题

## 🛡️ 关于反病毒软件误报的说明

本程序使用了 Nuitka/PyInstaller 工具进行封装（🔥**Coldfix 版使用pyinstaller封装，UPX压缩**）。由于压缩和封装方式与一些木马较为相似，部分反病毒软件在扫描时可能会将其误判为威胁。这种误报并非表示程序本身有问题，而是因为反病毒软件通过特征匹配判断出风险。

解决方案：

* 如果您希望避免误报，最稳妥的方式是：自行安装 Python 环境，从官方仓库克隆源代码后直接运行。

* 如果确实需要使用预编译版本，并且您信任本程序及开发者，也可以将程序添加到反病毒软件的白名单中。

* 本着安全第一的原则，如果确实对本程序及开发者不信任，请使用其他同类工具替代。

## 🔑 开源许可

本项目在 **MIT License** 许可协议下进行发布。

wbi 签名、部分接口以及 buvid3 等参数生成参考 [SocialSisterYi/bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)  

程序所提供的 FFmpeg 来源于 [https://github.com/ScottSloan/FFmpeg](https://github.com/ScottSloan/FFmpeg) 编译配置参见 `gccconf` 文件。  
Windows 编译版使用 [PyStand](https://github.com/skywind3000/PyStand) 进行封装。

## 🛠️ 参与贡献

欢迎提出新的点子~

<a href="https://github.com/ScottSloan/Bili23-Downloader/graphs/contributors" target="_blank">
    <img src="https://contrib.rocks/image?repo=ScottSloan/Bili23-Downloader" alt="Contributors" style="width: 300px"/>
</a>

Made with [contrib.rocks](https://contrib.rocks).

## 💪 支持我们

<img src="https://bili23.scott-sloan.cn/sponsor.png" alt="Sponser" style="width: 300px">

Bili23-Downloader 项目主要由作者 [Scott Sloan](https://github.com/ScottSloan) 在业余时间开发维护。  
如果这个项目对您有所帮助，您可以帮作者买一杯咖啡表示鼓励☕️，也可以点一个 ⭐️ 支持我们。

---

**修改版说明**：本 coldfix 版本由第三方开发者基于官方 v1.70.4 版本修改，主要增强了下载功能和便携性。再次感谢原作者 Scott Sloan 的优秀作品！
