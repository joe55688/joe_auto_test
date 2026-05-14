# Windows 11 Build Documentation

## 👍 快速開始 (Windows 11)

### 方式 1: 自動構建 (最簡單) ⭐

1. 打開 Windows 資源管理器
2. 進入 `joe_auto_test` 文件夾
3. **雙擊 `build.bat`**
4. 等待構建完成 (約 5-15 分鐘)
5. 在 `dist\` 文件夾中找到 `JoeAutoTest.exe`

### 方式 2: 命令行構建

在 PowerShell 或 CMD 中運行:

```powershell
# 進入項目目錄
cd C:\Path\To\joe_auto_test

# 運行構建
python build.py
```

### 方式 3: PyInstaller 直接命令

```powershell
cd C:\Path\To\joe_auto_test

pip install PyInstaller

pyinstaller ^^
  --onefile ^^
  --windowed ^^
  --name=JoeAutoTest ^^
  --add-data src:src ^^
  --hidden-import=pynput ^^
  --hidden-import=cv2 ^^
  --hidden-import=PyQt5 ^^
  --hidden-import=numpy ^^
  src\gui\main_window.py
```

---

## 📋 系統要求

- **OS**: Windows 11 (64-bit)
- **Python**: 3.8 或更高版本
- **硬盤空間**: 至少 2 GB 用於依賴和構建

### 安裝 Python

1. 訪問 https://www.python.org/downloads/
2. 下載 Python 3.11+
3. **重要**: 在安裝時勾選 "Add Python to PATH"
4. 點擊 "Install Now"

---

## 🚀 構建過程

### build.bat 將自動執行:

```
1. ✅ 檢查 Python 安裝
2. ✅ 安裝 PyInstaller
3. ✅ 清理舊構建文件
4. ✅ 編譯 Python 代碼為 .exe
5. ✅ 打包所有依賴
6. ✅ 生成最終可執行文件
```

---

## 📂 輸出文件

構建完成後，您會看到:

```
joe_auto_test/
├── dist/
│   └── JoeAutoTest.exe          ← 可執行文件 (150-200 MB)
├── build/                       ← 構建臨時文件
├── JoeAutoTest.spec             ← PyInstaller 配置
└── ...
```

---

## ▶️ 運行可執行文件

### 方式 1: 雙擊

在資源管理器中進入 `dist` 文件夾，雙擊 `JoeAutoTest.exe`

### 方式 2: 命令行

```powershell
.\dist\JoeAutoTest.exe
```

### 方式 3: 創建快捷方式

1. 右鍵點擊 `JoeAutoTest.exe`
2. 選擇 "發送到" → "桌面 (創建快捷方式)"
3. 雙擊桌面上的快捷方式

---

## 🔧 故障排查

### ❌ "Python not found"

**原因**: Python 未安裝或未在 PATH 中

**解決方案**:
1. 安裝 Python 3.8+
2. 重新啟動 CMD/PowerShell
3. 驗證: 運行 `python --version`

### ❌ "PyInstaller failed" 或 "No module named PyInstaller"

**原因**: PyInstaller 未安裝或版本過舊

**解決方案**:
```powershell
pip install --upgrade PyInstaller
python build.py
```

### ❌ "缺少模塊" 錯誤

**原因**: 某些依賴模塊未正確打包

**解決方案**:
```powershell
pip install -r requirements.txt
pip install -r requirements-build.txt
python build.py
```

### ❌ 構建很慢

**原因**: 首次構建需要編譯所有依賴

**解決方案**: 第一次構建需要 5-15 分鐘，之後重新構建會更快

### ❌ .exe 文件過大 (> 500 MB)

**原因**: 包含了不必要的依賴

**解決方案**: 編輯 `build.py` 刪除多餘的 `--hidden-import` 參數

---

## ✨ 關於生成的 .exe

✅ **獨立可執行** - 不需要 Python 環境  
✅ **一鍵運行** - 雙擊即可  
✅ **完整功能** - 所有功能都可用  
✅ **無需安裝** - 解壓即用  
✅ **跨機器運行** - 可複製到其他 Windows 11 電腦

---

## 📊 文件大小參考

| 組件 | 大小 |
|------|------|
| Python 運行時 | ~50 MB |
| PyQt5 | ~30 MB |
| OpenCV | ~50 MB |
| NumPy/SciPy | ~30 MB |
| 其他依賴 | ~10 MB |
| **總計** | **~170 MB** |

---

## 📝 最佳實踐

1. **第一次構建**: 允許 10-15 分鐘完成
2. **網絡連接**: 確保有穩定的網絡
3. **硬盤空間**: 至少 3 GB 可用空間
4. **防病毒軟件**: 某些防病毒軟件可能干擾構建
5. **系統更新**: 保持 Windows 11 最新

---

## 🎯 高級配置

### 自定義圖標

編輯 `build.py`，替換:
```python
"--icon=NONE",
```

為:
```python
"--icon=path/to/icon.ico",
```

### 添加版本信息

編輯 `build.py`，添加:
```python
"--version-file=version_info.txt",
```

---

## 📞 支持

如有問題，請:

1. 查看本文檔的故障排查部分
2. 檢查 GitHub Issues: https://github.com/joe55688/joe_auto_test/issues
3. 確保依賴已正確安裝

---

**祝構建順利！** 🚀
