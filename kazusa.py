import re
import sys
import os
import asyncio
import threading
import aiohttp

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QFileDialog, QPlainTextEdit,
    QProgressBar, QComboBox, QSpinBox, QDialog, QSizePolicy, QListWidget,
    QMessageBox, QListWidgetItem, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QTimer, QSettings
from PyQt6.QtGui import QIcon, QFont, QPalette, QBrush, QPixmap

from threading import Thread, Event

# 由於打包後模組結構會改變，需要確保能正確匯入
try:
    from scraper.kemono import extract_attachments_urls_by_id, get_post_choices
    from downloader.downloader_concurrent import download_streamed_posts
    from utils.update_status import update_status
except ImportError:
    # 處理打包後可能發生的相對路徑問題（雖然 Nuitka 通常處理得很好）
    print("無法匯入自訂模組，請檢查打包設定。")
    sys.exit(1)


ANNOUNCEMENT_URL = "https://gist.githubusercontent.com/slbidd/8fc6b2357a7b5b6915ad6a2297d776ca/raw/announcement.txt"


class DownloadWorker(QObject):
    log_signal = pyqtSignal(str) 
    finish_signal = pyqtSignal()
    post_progress_signal = pyqtSignal(int)
    post_max_signal = pyqtSignal(int)
    file_progress_signal = pyqtSignal(int)
    file_max_signal = pyqtSignal(int)
    error_signal = pyqtSignal(list)

    def __init__(self, url, path, selected_ids, day_mode, parallel):
        super().__init__()
        self.url = url
        self.path = path
        self.selected_ids = selected_ids
        self.day_mode = day_mode
        self.parallel = parallel
        self.pause_event = Event()
        self.pause_event.set()
        self.stop_event = Event()

    def make_logger_with_error(self):
        def logger_with_error(msg):
            print(msg) 
            self.log_signal.emit(msg)
            # 錯誤日誌的解析和發射應該由 downloader 內部完成，這裡簡化處理
            # 避免UI層級的程式碼去解析日誌字串來判斷錯誤
            # if msg.startswith("❌") or msg.startswith("⚠️"):
            #     match = re.search(r"(C:/[^\s]+)", msg)
            #     if match and hasattr(self, "error_signal"):
            #         self.error_signal.emit([match.group(1)])
        return logger_with_error

    def start(self):
        Thread(target=self.run, daemon=True).start()

    def run(self):
        asyncio.run(self._main())

    async def _main(self):
        try:
            post_stream = extract_attachments_urls_by_id(
                self.url, selected_ids=self.selected_ids, day_mode=self.day_mode
            )
            await download_streamed_posts(
                url=self.url,
                post_stream=post_stream,
                base_path=self.path,
                concurrency=self.parallel,
                update_status=update_status,
                pause_event=self.pause_event,
                stop_event=self.stop_event,
                logger=self.make_logger_with_error(),
                signal_host=self,
                error_signal=self.error_signal,
                day_mode=self.day_mode,
                selected_ids=self.selected_ids
            )
        except Exception as e:
            print(f"下載出錯: {e}")
            self.log_signal.emit(f"❌ 下載執行緒發生嚴重錯誤: {e}")
        self.finish_signal.emit()

    def pause(self):
        self.pause_event.clear()

    def resume(self):
        self.pause_event.set()

    def stop(self):
        self.stop_event.set()
        self.pause_event.set()


class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("設定")
        self.setFixedSize(320, 200)

        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                font-size: 11pt;
                color: #cdd6f4;
            }
            QSpinBox, QComboBox {
                background-color: #313244;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 6px;
                padding: 5px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 18px;
            }
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #a6e3a1;
            }
            QPushButton:pressed {
                background-color: #94e2d5;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        row1 = QHBoxLayout()
        label_parallel = QLabel("最大併發數:")
        row1.addWidget(label_parallel)
        row1.addStretch()
        self.spin_parallel = QSpinBox()
        self.spin_parallel.setRange(1, 50)
        self.spin_parallel.setValue(parent.max_parallel)
        row1.addWidget(self.spin_parallel)
        layout.addLayout(row1)

        row2 = QHBoxLayout()
        label_date = QLabel("日期命名模式:")
        row2.addWidget(label_date)
        row2.addStretch()
        self.date_mode = QComboBox()
        self.date_mode.addItems(["無", "日期前綴", "日期後綴"])
        self.date_mode.setCurrentIndex(parent.day_mode)
        row2.addWidget(self.date_mode)
        layout.addLayout(row2)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn = QPushButton("套用設定")
        btn.clicked.connect(self.apply)
        btn_layout.addWidget(btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def apply(self):
        self.parent().max_parallel = self.spin_parallel.value()
        self.parent().day_mode = self.date_mode.currentIndex()
        self.accept()
        print(f"🧪 設定完成，day_mode = {self.parent().day_mode}")


class SelectorDialog(QDialog):
    posts_ready = pyqtSignal(list)
    def __init__(self, url, day_mode):
        super().__init__()
        self.setWindowTitle("篩選貼文")
        self.resize(600, 450)
        self.selected_ids = []

        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2e;
                color: #cdd6f4;
            }
            QListWidget {
                background-color: #181825;
                border: 1px solid #45475a;
                border-radius: 6px;
            }
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #a6e3a1;
            }
        """)

        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.btn_confirm = QPushButton("✅ 確認並開始下載")
        self.btn_confirm.clicked.connect(self.apply)
        layout.addWidget(self.btn_confirm)

        self.posts_ready.connect(self.on_posts_ready)
        self.load_posts_async(url, day_mode)

    def load_posts_async(self, url, day_mode):
        def worker():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                posts = loop.run_until_complete(get_post_choices(url, day_mode))
                loop.close()
            except Exception as e:
                print(f"[❌ 異常] 貼文拉取失敗: {e}")
                self.posts_ready.emit([])
                QTimer.singleShot(0, lambda: QMessageBox.warning(self, "加載失敗", f"獲取貼文失敗: {e}"))
                return
            self.posts_ready.emit(posts)
        threading.Thread(target=worker, daemon=True).start()

    def on_posts_ready(self, posts):
        self.posts = posts
        self.update_ui()

    def update_ui(self):
        self.list_widget.clear()
        for p in getattr(self, "posts", []):
            item = QListWidgetItem(p["display"])
            item.setData(1000, p["id"])
            item.setCheckState(Qt.CheckState.Unchecked)
            self.list_widget.addItem(item)

    def apply(self):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                self.selected_ids.append(item.data(1000))
        self.accept()


class MainPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.worker = None
        self.failed_files = []
        self.file_done = 0
        self.file_total = 0
        self.selected_ids = None

        self._apply_stylesheet()
        self._init_ui()
        self._connect_signals()

    def _apply_stylesheet(self):
        self.setStyleSheet("""
            QWidget#MainPage {
                color: #cdd6f4;
                font-family: 'Segoe UI', sans-serif;
                font-size: 10pt;
            }
            QFrame#ControlPanel {
                background-color: rgba(30, 30, 46, 190);
                border: 1px solid #45475a;
                border-radius: 8px;
            }
            QLabel {
                background-color: transparent;
                color: #cdd6f4;
            }
            QLineEdit {
                background-color: #313244;
                border: 1px solid #45475a;
                border-radius: 6px;
                padding: 8px;
                color: #cdd6f4;
            }
            QLineEdit:focus {
                border: 1px solid #89b4fa;
            }
            QProgressBar {
                border: 1px solid #45475a;
                border-radius: 6px;
                text-align: center;
                background-color: #313244;
                color: #cdd6f4;
            }
            QProgressBar::chunk {
                background-color: #a6e3a1;
                border-radius: 5px;
            }
            QPushButton {
                border: 1px solid #45475a;
                border-radius: 6px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton#Primary {
                background-color: #89b4fa;
                color: #1e1e2e;
                border: 1px solid #89b4fa;
            }
            QPushButton#Primary:hover {
                background-color: #a6e3a1;
                border-color: #a6e3a1;
            }
            QPushButton#Secondary {
                background-color: #45475a;
                color: #cdd6f4;
            }
            QPushButton#Secondary:hover {
                background-color: #585b70;
            }
            QPushButton#Danger {
                background-color: #f38ba8;
                color: #1e1e2e;
                border-color: #f38ba8;
            }
            QPushButton#Danger:hover {
                background-color: #eba0ac;
            }
            /* <<< 新增 QPlainTextEdit 的樣式 >>> */
            QPlainTextEdit {
                background-color: #181825;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 6px;
                font-family: 'Consolas', 'Courier New', monospace;
            }
        """)

    def _init_ui(self):
        self.setObjectName("MainPage")
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # --- 控制面板 ---
        control_panel = QFrame()
        control_panel.setObjectName("ControlPanel")
        control_panel.setMaximumWidth(400)
        left_layout = QVBoxLayout(control_panel)
        left_layout.setContentsMargins(15, 15, 15, 15)
        left_layout.setSpacing(15)

        title = QLabel("Kemono 下載器")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18pt; font-weight: bold; color: #89b4fa; border: none;")
        left_layout.addWidget(title)
        
        url_layout = QHBoxLayout()
        self.url = QLineEdit()
        self.url.setPlaceholderText("請輸入作者主頁網址")
        url_layout.addWidget(QLabel("主頁:"))
        url_layout.addWidget(self.url)
        left_layout.addLayout(url_layout)

        path_layout = QHBoxLayout()
        self.path = QLineEdit()
        self.path.setPlaceholderText("選擇儲存資料夾")
        btn_path = QPushButton("瀏覽...")
        btn_path.setObjectName("Secondary")
        btn_path.clicked.connect(self.select_path)
        path_layout.addWidget(QLabel("路徑:"))
        path_layout.addWidget(self.path)
        path_layout.addWidget(btn_path)
        left_layout.addLayout(path_layout)

        self.btn_select = QPushButton("篩選貼文")
        self.btn_select.setObjectName("Secondary")
        left_layout.addWidget(self.btn_select)
        
        left_layout.addSpacing(10)

        controls_layout = QHBoxLayout()
        self.btn_start = QPushButton("開始下載")
        self.btn_start.setObjectName("Primary")
        self.btn_pause = QPushButton("暫停")
        self.btn_pause.setObjectName("Secondary")
        self.btn_resume = QPushButton("繼續")
        self.btn_resume.setObjectName("Secondary")
        self.btn_stop = QPushButton("停止")
        self.btn_stop.setObjectName("Danger")

        controls_layout.addWidget(self.btn_start)
        controls_layout.addWidget(self.btn_pause)
        controls_layout.addWidget(self.btn_resume)
        controls_layout.addWidget(self.btn_stop)

        left_layout.addLayout(controls_layout)

        # --- 進度顯示 ---
        progress_layout = QVBoxLayout()
        self.file_progress_label = QLabel("檔案進度: 0 / 0")
        self.file_progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress = QProgressBar()
        
        progress_layout.addWidget(self.file_progress_label)
        progress_layout.addWidget(self.progress)
        
        # <<< 新增：建立日誌輸出框 >>>
        self.log_output_label = QLabel("執行日誌:")
        self.log_output = QPlainTextEdit()
        self.log_output.setReadOnly(True)
        progress_layout.addWidget(self.log_output_label)
        progress_layout.addWidget(self.log_output)
        
        left_layout.addLayout(progress_layout)

        left_layout.addStretch()

        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        self.btn_error = QPushButton("查看失敗項目")
        self.btn_error.setObjectName("Secondary")
        self.btn_settings = QPushButton("設定")
        self.btn_settings.setObjectName("Secondary")
        footer_layout.addWidget(self.btn_error)
        footer_layout.addWidget(self.btn_settings)
        left_layout.addLayout(footer_layout)

        main_layout.addWidget(control_panel)
        main_layout.addStretch()

        self.btn_pause.setEnabled(False)
        self.btn_resume.setEnabled(False)
        self.btn_stop.setEnabled(False)
    
    def _connect_signals(self):
        self.btn_start.clicked.connect(self.start_download)
        self.btn_pause.clicked.connect(self.pause_download)
        self.btn_resume.clicked.connect(self.resume_download)
        self.btn_stop.clicked.connect(self.stop_download)
        self.btn_settings.clicked.connect(self.open_settings)
        self.btn_error.clicked.connect(self.show_failed)
        self.btn_select.clicked.connect(self.open_selector)
    
    def update_ui_state(self, is_running):
        self.btn_start.setEnabled(not is_running)
        self.btn_select.setEnabled(not is_running)
        self.btn_pause.setEnabled(is_running)
        self.btn_stop.setEnabled(is_running)
        self.btn_resume.setEnabled(False)

    def select_path(self):
        path = QFileDialog.getExistingDirectory(self, "選擇儲存目錄")
        if path:
            self.path.setText(path)

    def start_download(self):
        # <<< 新增：開始下載時清空舊的日誌 >>>
        self.log_output.clear()
        
        self.file_total = 0
        self.file_done = 0
        self.failed_files = []
        self.update_file_progress(0) # 重置計數
        self.progress.setValue(0)
        self.progress.setMaximum(100) # 先設為100，避免除以0

        url = self.url.text().strip()
        path = self.path.text().strip()
        if not url or not path:
            QMessageBox.warning(self, "輸入錯誤", "請輸入有效的 URL 和儲存路徑！")
            return
        
        self.worker = DownloadWorker(
            url, path, self.selected_ids,
            self.main.day_mode,
            self.main.max_parallel,
        )
        self.worker.setParent(self)
        
        # <<< 修改：連接 log_signal 到新的槽函式 >>>
        self.worker.log_signal.connect(self.append_log)
        self.worker.file_max_signal.connect(self.update_file_max)
        self.worker.file_progress_signal.connect(self.update_file_progress)
        self.worker.error_signal.connect(self.collect_failed)
        self.worker.finish_signal.connect(lambda: self.update_ui_state(False))

        self.worker.start()
        self.update_ui_state(True)
        self.append_log("▶️ 下載任務已啟動！")

    # <<< 新增：用於接收日誌並更新UI的槽函式 >>>
    def append_log(self, text):
        self.log_output.appendPlainText(text)
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())


    def pause_download(self):
        if self.worker:
            self.worker.pause()
            self.append_log("⏸️ 任務已暫停")
            self.btn_pause.setEnabled(False)
            self.btn_resume.setEnabled(True)

    def resume_download(self):
        if self.worker:
            self.worker.resume()
            self.append_log("▶️ 任務已繼續")
            self.btn_pause.setEnabled(True)
            self.btn_resume.setEnabled(False)

    def stop_download(self):
        if self.worker:
            self.worker.stop()
            self.append_log("⛔️ 已傳送終止訊號，請稍候...")
            self.update_ui_state(False)

    def open_settings(self):
        dlg = SettingsDialog(self.main)
        dlg.exec()

    def update_file_max(self, n):
        self.file_total += n
        self.progress.setMaximum(self.file_total if self.file_total > 0 else 100)
        self.file_progress_label.setText(f"檔案進度: {self.file_done} / {self.file_total}")
    
    def update_file_progress(self, n=1):
        if self.file_total == 0: # 避免在 file_max_signal 抵達前更新
            return
        self.file_done += n
        self.progress.setValue(self.file_done)
        self.file_progress_label.setText(f"檔案進度: {self.file_done} / {self.file_total}")

    def collect_failed(self, file_infos):
        self.failed_files.extend(file_infos)

    def show_failed(self):
        if not self.failed_files:
            QMessageBox.information(self, "提示", "🎉 沒有失敗的檔案")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("下載失敗文件列表")
        layout = QVBoxLayout(dialog)

        list_widget = QListWidget()
        for line in self.failed_files:
            if "|" in line:
                path, url = line.split("|", 1)
                display = f"❌ {os.path.basename(path.strip())}\n📂 路徑: {path.strip()}\n🌐 連結: {url.strip()}"
            else:
                display = line
            item = QListWidgetItem(display)
            list_widget.addItem(item)
        layout.addWidget(list_widget)

        btns = QHBoxLayout()
        copy_btn = QPushButton("複製全部")
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText('\n'.join(self.failed_files)))
        btns.addWidget(copy_btn)

        close_btn = QPushButton("關閉")
        close_btn.clicked.connect(dialog.accept)
        btns.addWidget(close_btn)

        layout.addLayout(btns)
        dialog.resize(700, 450)
        dialog.exec()

    def open_selector(self):
        url = self.url.text().strip()
        if not url:
            QMessageBox.warning(self, "錯誤", "請先填寫主頁網址")
            return

        dlg = SelectorDialog(self.url.text().strip(), self.main.day_mode)
        if dlg.exec():
            self.selected_ids = dlg.selected_ids
            if self.selected_ids:
                msg = f"已選擇 {len(self.selected_ids)} 條貼文"
                QMessageBox.information(self, "提示", msg)
                self.append_log(f"ℹ️ {msg}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # --- 解決打包後資源路徑問題的核心程式碼 ---
        if getattr(sys, 'frozen', False):
            # 如果是打包後的 .exe
            self.base_path = os.path.dirname(sys.executable)
        else:
            # 如果是直接執行 .py
            self.base_path = os.path.dirname(__file__)
        
        icon_path = os.path.join(self.base_path, "Bocchi 1.ico")
        self.background_image_path = os.path.join(self.base_path, "1.jpg")
        
        if os.path.exists(icon_path):
                 self.setWindowIcon(QIcon(icon_path))
        
        self.setWindowTitle("Kemono 下載器v1.0")
        self.resize(1100, 650)
        self.setMinimumSize(900, 600)
        
        self.day_mode = 1
        self.max_parallel = 10
        
        self.main_page = MainPage(self)
        self.setCentralWidget(self.main_page)

        # 設定背景圖片
        self.setAutoFillBackground(True)
        self.update_background()

        self.load_settings() # 呼叫讀取設定的函式

    def load_settings(self):
        """在程式啟動時，讀取並套用儲存的設定"""
        # "kazusa777", "kemonodownloader" 是為了讓 QSettings 知道在哪裡儲存設定
        # 您可以換成您喜歡的名稱
        settings = QSettings("kazusa777", "kemonodownloader")
        
        # 讀取名為 "downloadPath" 的設定，如果不存在，則預設為空字串 ""
        saved_path = settings.value("downloadPath", "")
        
        # 將讀取到的路徑設定到 UI 的輸入框中
        self.main_page.path.setText(saved_path)
        print(f"ℹ️ 已讀取上次儲存的路徑: {saved_path}")

    def update_background(self):
        palette = self.palette()
        pixmap = QPixmap(self.background_image_path)
        if not pixmap.isNull():
            palette.setBrush(QPalette.ColorRole.Window, QBrush(
                pixmap.scaled(
                    self.size(), 
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                    Qt.TransformationMode.SmoothTransformation
                )
            ))
        self.setPalette(palette)

    def resizeEvent(self, event):
        # 視窗大小改變時，重新縮放並設定背景
        self.update_background()
        super().resizeEvent(event)

    def save_settings(self):
        """儲存目前的設定"""
        settings = QSettings("kazusa777", "kemonodownloader")
        
        # 獲取目前路徑輸入框的文字
        current_path = self.main_page.path.text()
        
        # 將路徑儲存到名為 "downloadPath" 的設定中
        settings.setValue("downloadPath", current_path)
        print(f"ℹ️ 已儲存當前路徑: {current_path}")

    def closeEvent(self, event):
        """當使用者關閉視窗時，自動觸發此事件"""
        self.save_settings() # 在關閉前儲存設定
        super().closeEvent(event) # 繼續執行原本的關閉流程



if __name__ == "__main__":
    # 為了方便測試，我將您的下載邏輯用模擬函式替換了
    # 您可以將 try...except 區塊還原成您原本的樣子來使用
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
