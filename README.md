# Joe Auto Test - OS自動化測試工具

一個功能完整的鍵盤和滑鼠操作錄製、回放、截圖比對的自動化測試框架。

## 功能特性

✨ **操作錄製**
- 實時錄製鍵盤和滑鼠操作
- 精確時間戳記錄
- 支持多種鍵盤按鍵和滑鼠事件

🔄 **智能回放**
- 按照原始時間間隔回放操作
- 支持調整回放速度
- 實時日誌輸出

📸 **截圖比對**
- 自動擷取關鍵畫面
- 圖像相似度匹配算法
- 支持區域截圖和全屏截圖

📋 **腳本管理**
- GUI界面管理多個錄製腳本
- 支持腳本編輯和刪除
- 腳本版本控制

🖥️ **跨平台支持**
- Windows 支持
- Linux 支持
- 統一的GUI界面

## 系統要求

- Python 3.8+
- Windows 10+ 或 Ubuntu 20.04+
- pip (Python 包管理器)

## 快速安裝

### 1. 克隆倉庫
```bash
git clone https://github.com/joe55688/joe_auto_test.git
cd joe_auto_test
```

### 2. 安裝依賴
```bash
pip install -r requirements.txt
```

### 3. 運行應用
```bash
python -m src.gui.main_window
```

## 快速開始

### 1️⃣ 錄製新腳本
- 啟動應用程序
- 點擊 "New Recording" 選項卡
- 輸入腳本名稱
- 點擊 "Start Recording"
- 執行您想錄製的操作
- 點擊 "Stop Recording"

### 2️⃣ 回放腳本
- 點擊 "Playback" 選項卡
- 從列表中選擇腳本
- 調整速度滑塊 (0.5x - 2.0x)
- 點擊 "Start Playback"

### 3️⃣ 截圖比對
- 點擊 "Screenshot" 選項卡
- 選擇要比對的兩張圖像
- 查看相似度結果

## 項目結構

```
joe_auto_test/
├── README.md                 # 項目說明
├── requirements.txt          # Python依賴
├── src/
│   ├── __init__.py
│   ├── recorder.py           # 操作錄製模塊
│   ├── player.py             # 操作回放模塊
│   ├── screenshot_matcher.py # 截圖比對模塊
│   ├── script_manager.py     # 腳本管理模塊
│   ├── config.py             # 配置文件
│   └── gui/
│       ├── __init__.py
│       └── main_window.py    # GUI主界面
├── scripts/                  # 保存的腳本
├── screenshots/              # 保存的截圖
└── .gitignore
```

## 依賴庫

- `pynput` - 鍵盤/滑鼠監聽和控制
- `Pillow` - 圖像處理
- `opencv-python` - 截圖比對和圖像分析
- `PyQt5` - GUI框架
- `numpy` - 數值計算

## 配置

編輯 `src/config.py` 自定義設置：

```python
# 截圖比對相似度閾值 (0-1)
SIMILARITY_THRESHOLD = 0.85

# 回放速度範圍
MIN_PLAYBACK_SPEED = 0.5
MAX_PLAYBACK_SPEED = 2.0

# 腳本存儲路徑
SCRIPTS_DIR = "./scripts"

# 截圖存儲路徑
SCREENSHOTS_DIR = "./screenshots"
```

## 許可證

MIT License

## 聯繫

如有問題或建議，請提交 GitHub Issue。

---

**開發者**: joe55688  
**最後更新**: 2026-05-14
