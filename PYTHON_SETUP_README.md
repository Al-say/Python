# Python 环境设置

## 环境变量设置

### 自动设置脚本

项目中包含了两个脚本文件，用于快速设置Python 3.13.11为默认版本：

#### Windows批处理文件 (set_python313.bat)
```cmd
# 双击运行或在命令提示符中运行
set_python313.bat
```

#### PowerShell脚本 (set_python313.ps1)
```powershell
# 在PowerShell中运行
.\set_python313.ps1
```

### 手动设置方法

如果脚本不能正常工作，可以手动设置环境变量：

1. 打开系统环境变量设置
2. 在"用户变量"或"系统变量"中找到"Path"
3. 将以下路径添加到Path变量的开头：
   ```
   C:\Users\Administrator\AppData\Local\Programs\Python\Python313\Scripts\
   C:\Users\Administrator\AppData\Local\Programs\Python\Python313\
   ```

### 验证设置

运行以下命令验证设置是否成功：
```bash
python --version    # 应显示 Python 3.13.11
pip --version       # 应显示 python 3.13
```

## 当前环境状态

- **Python版本**: 3.13.11 (最新稳定版)
- **Pip版本**: 25.3
- **安装包**: NumPy, Pandas, Matplotlib, Seaborn, Scikit-learn, Jupyter等

## 使用建议

1. 优先使用 `python` 命令（已设置为3.13.11）
2. 如需使用旧版本，可使用 `py -3.11` 命令
3. 机器学习项目可在 `machine_learning/` 目录下继续开发
