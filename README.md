<img width="2380" height="1678" alt="ask1" src="https://github.com/user-attachments/assets/275fe3ac-35f4-46f5-ad25-734819b45dd2" />
<img width="2476" height="1604" alt="ask2" src="https://github.com/user-attachments/assets/f4c621a4-ea66-49e5-8035-b37cfcc7006a" />
# geogebra-3d-app
A small tool


---

## 📢 关于安装包体积的说明 / About App Size

* **中文说明**：本工具解压后体积较大（约 2GB），是因为内嵌了完整的 Chromium 浏览器内核 (`PyQt6.QtWebEngine`)。经测试，macOS 自带的 Safari 浏览器对 Plotly 3D WebGL 的隐函数等值面兼容性较差（会导致画面卡死、错位）。内置谷歌内核是为了确保所有 Mac 用户都能获得 100% 稳定、丝滑的 3D 绘图体验。未来版本将进行轻量化重构。
* **English Notice**: The unzipped bundle is around 2GB because it embeds a full Chromium browser core (`PyQt6.QtWebEngine`). Standard Safari on macOS suffers from rendering freezes when handling Plotly's 3D WebGL Isosurfaces. Embedding Chromium ensures a 100% stable, flawless 3D plotting experience out of the box. A lightweight refactor is planned for the next release.



---

## 🛠️ 自行编译指南 / How to Build from Source (For Windows & Linux)

### 中文指南：
如果你使用的是 Windows 或 Linux 系统，可以通过以下命令在本地一分钟内自行打包生成对应的可执行文件：

1. **配置环境**（推荐在 Anaconda 或纯净虚拟环境中运行）：
   ```bash
   pip install numpy sympy plotly pyinstaller PyQt6 PyQt6-WebEngine
   ```
2. **执行本地打包命令**：
   ```bash
   pyinstaller --onedir --windowed --name="MyGeoGebra3D_Local" --collect-all PyQt6.QtWebEngineWidgets my_geogebra_app.py
   ```
3. 打包完成后，即可在本地生成的 `dist/MyGeoGebra3D_Local` 文件夹内直接双击运行。

---

### English Guide:
If you are on Windows or Linux, you can easily build the executable locally in less than a minute by following these steps:

1. **Environment Setup** (Recommended inside an Anaconda or clean venv environment):
   ```bash
   pip install numpy sympy plotly pyinstaller PyQt6 PyQt6-WebEngine
   ```
2. **Run PyInstaller Command**:
   ```bash
   pyinstaller --onedir --windowed --name="MyGeoGebra3D_Local" --collect-all PyQt6.QtWebEngineWidgets my_geogebra_app.py
   ```
3. Once completed, navigate to the `dist/MyGeoGebra3D_Local` folder and double-click the generated application to run it.
