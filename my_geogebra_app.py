import sys
import os
import random
import tempfile  # 🌟 新增：引入系统临时文件库
import numpy as np
import sympy as sp
import plotly.graph_objects as go
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtWebEngineWidgets import QWebEngineView

class MathPlotterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D 隐函数绘图仪 (Marching Cubes 空间坐标系+立体箭头版)")
        self.setGeometry(100, 100, 1200, 850)
        self.last_html_file = ""
        self.init_ui()
        self.generate_math_plot()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # 控制面板布局
        control_panel = QWidget()
        control_panel.setFixedWidth(320)
        control_layout = QVBoxLayout(control_panel)

        control_layout.addWidget(QLabel("<b>方程 f(x,y,z)=0:</b>"))
        self.equation_input = QLineEdit("x^2 + y^2 - z")
        control_layout.addWidget(self.equation_input)

        for name, default in [("X", "-4, 4"), ("Y", "-4, 4"), ("Z", "-4, 4")]:
            control_layout.addWidget(QLabel(f"<b>{name} 轴范围 (min, max):</b>"))
            setattr(self, f"{name.lower()}_range", QLineEdit(default))
            control_layout.addWidget(getattr(self, f"{name.lower()}_range"))

        self.plot_button = QPushButton("🚀 提取网格等值面")
        self.plot_button.setStyleSheet("background-color: #E65100; color: white; font-weight: bold; font-size: 14px; padding: 8px;")
        self.plot_button.clicked.connect(self.generate_math_plot)
        control_layout.addWidget(self.plot_button)

        control_layout.addStretch()
        main_layout.addWidget(control_panel)

        self.web_view = QWebEngineView()
        main_layout.addWidget(self.web_view)

    def generate_math_plot(self):
        try:
            # 1. 精准解析输入范围
            eq_text = self.equation_input.text()
            x_min, x_max = map(float, self.x_range.text().split(','))
            y_min, y_max = map(float, self.y_range.text().split(','))
            z_min, z_max = map(float, self.z_range.text().split(','))

            x_sym, y_sym, z_sym = sp.symbols('x y z')
            math_func = sp.lambdify((x_sym, y_sym, z_sym), sp.sympify(eq_text), 'numpy')

            # 建立三维立体点云网格
            X, Y, Z = np.mgrid[x_min:x_max:60j, y_min:y_max:60j, z_min:z_max:60j]
            Values = np.real(math_func(X, Y, Z)).astype(float)

            # 2. 创建画布
            fig = go.Figure()

            # 3. 绘制隐函数等值面
            fig.add_trace(go.Isosurface(
                x=X.flatten(), y=Y.flatten(), z=Z.flatten(),
                value=Values.flatten(),
                isomin=-0.1, isomax=0.1,
                surface_count=5,
                colorscale='Plasma',
                showscale=True,
                caps=dict(x_show=False, y_show=False, z_show=False),
                contour=dict(show=True, color='white', width=2),
                lighting=dict(ambient=0.6, diffuse=0.8, specular=0.5, roughness=0.3),
                name="f(x,y,z)=0"
            ))

            # 4. 绘制三维直角坐标系轴线 (X=红, Y=绿, Z=蓝)
            # X 轴线
            fig.add_trace(go.Scatter3d(
                x=[x_min, x_max], y=[0, 0], z=[0, 0],
                mode='lines+text', text=["", "X"], textposition="top center",
                line=dict(color='red', width=5), name='X 轴', showlegend=False
            ))
            # Y 轴线
            fig.add_trace(go.Scatter3d(
                x=[0, 0], y=[y_min, y_max], z=[0, 0],
                mode='lines+text', text=["", "Y"], textposition="top center",
                line=dict(color='green', width=5), name='Y 轴', showlegend=False
            ))
            # Z 轴线
            fig.add_trace(go.Scatter3d(
                x=[0, 0], y=[0, 0], z=[z_min, z_max],
                mode='lines+text', text=["", "Z"], textposition="top center",
                line=dict(color='blue', width=5), name='Z 轴', showlegend=False
            ))

            # 🌟 5. 核心：动态计算并绘制立体圆锥箭头
            arrow_size = (x_max - x_min) * 0.05  # 箭头大小取轴全长的 5%
            # X 轴红箭头
            fig.add_trace(go.Cone(
                x=[x_max], y=[0], z=[0], u=[1], v=[0], w=[0],
                colorscale=[[0, 'red'], [1, 'red']], showscale=False,
                sizemode='absolute', sizeref=arrow_size, anchor='tip', showlegend=False
            ))
            # Y 轴绿箭头
            fig.add_trace(go.Cone(
                x=[0], y=[y_max], z=[0], u=[0], v=[1], w=[0],
                colorscale=[[0, 'green'], [1, 'green']], showscale=False,
                sizemode='absolute', sizeref=arrow_size, anchor='tip', showlegend=False
            ))
            # Z 轴蓝箭头
            fig.add_trace(go.Cone(
                x=[0], y=[0], z=[z_max], u=[0], v=[0], w=[1],
                colorscale=[[0, 'blue'], [1, 'blue']], showscale=False,
                sizemode='absolute', sizeref=arrow_size, anchor='tip', showlegend=False
            ))

            # 6. 注入自由相机与布局调整
            fig.update_layout(
                dragmode='orbit',
                scene=dict(
                    xaxis=dict(range=[x_min, x_max], title='X 轴', showgrid=True, zeroline=False),
                    yaxis=dict(range=[y_min, y_max], title='Y 轴', showgrid=True, zeroline=False),
                    zaxis=dict(range=[z_min, z_max], title='Z 轴', showgrid=True, zeroline=False),
                    aspectmode='cube'
                ),
                margin=dict(l=0, r=0, b=0, t=0)
            )

            # 🌟 7. 优化变动：利用系统的 Temp 文件夹彻底避开 Mac 只读文件沙盒限制
            if self.last_html_file and os.path.exists(self.last_html_file):
                try:
                    os.remove(self.last_html_file)
                except:
                    pass

            # 获取系统临时目录，确保具备完整的写权限
            temp_dir = tempfile.gettempdir()
            temp_html = os.path.join(temp_dir, f"app_render_v_{random.randint(1000, 9999)}.html")
            
            # 写入并由 Web 视图加载
            fig.write_html(temp_html, include_plotlyjs=True)
            self.web_view.setUrl(QUrl.fromLocalFile(os.path.realpath(temp_html)))
            self.last_html_file = temp_html

        except Exception as e:
            QMessageBox.critical(self, "解析错误", f"方程有误！\n详情: {str(e)}")

    def closeEvent(self, event):
        if self.last_html_file and os.path.exists(self.last_html_file):
            try:
                os.remove(self.last_html_file)
            except:
                pass
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MathPlotterApp()
    window.show()
    sys.exit(app.exec())

