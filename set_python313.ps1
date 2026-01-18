# 设置Python 3.13为默认版本
$python313Path = "C:\Users\Administrator\AppData\Local\Programs\Python\Python313"
$python313Scripts = "C:\Users\Administrator\AppData\Local\Programs\Python\Python313\Scripts"

# 将Python 3.13路径添加到PATH开头
$env:PATH = $python313Scripts + ";" + $python313Path + ";" + $env:PATH

Write-Host "Python 3.13.11 已设置为默认版本" -ForegroundColor Green
python --version
Write-Host "Pip版本:" -ForegroundColor Yellow
pip --version
