# geogebra-3d-app
A small tool


---

## 📢 关于安装包体积的说明 / About App Size

* **中文说明**：本工具解压后体积较大（约 2GB），是因为内嵌了完整的 Chromium 浏览器内核 (`PyQt6.QtWebEngine`)。经测试，macOS 自带的 Safari 浏览器对 Plotly 3D WebGL 的隐函数等值面兼容性较差（会导致画面卡死、错位）。内置谷歌内核是为了确保所有 Mac 用户都能获得 100% 稳定、丝滑的 3D 绘图体验。未来版本将进行轻量化重构。
* **English Notice**: The unzipped bundle is around 2GB because it embeds a full Chromium browser core (`PyQt6.QtWebEngine`). Standard Safari on macOS suffers from rendering freezes when handling Plotly's 3D WebGL Isosurfaces. Embedding Chromium ensures a 100% stable, flawless 3D plotting experience out of the box. A lightweight refactor is planned for the next release.
