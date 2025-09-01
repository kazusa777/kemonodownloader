<h1>打包步驟</h1>

<blockquote>
<p><strong>特別聲明與致謝</strong></p>
<p>本工具的原始版本由 Bilibili 創作者「<a href="https://www.bilibili.com/video/BV1TjKKztELJ/" target="_blank"><strong>比逗逗丶</strong></a>」所開發。因原版在本人電腦上無法使用，此版本是基於其在dc社群分享的原始碼修改而來，以供個人學習。本人僅為修改者，並非原始開發者。</p>
<p>本倉庫之內容，係為個人進行學術研究與資料探討而設立，其目的僅限於技術分析與學術交流，不涉及任何商業利益或非法活動之圖利。任何使用者不得將本倉庫之資料用於任何非法、不道德或具爭議性之行為，並應自行承擔所有因不當利用本平台資料所產生之法律責任與風險。</p>
</blockquote>

<hr>

<p>這是一份關於如何使用 Nuitka 將 Python 專案打包成獨立可執行檔 (.exe) 的簡易操作說明。本指南將引導您從安裝 Python 環境開始，到最終完成編譯。</p>

<h2 id="目錄">目錄</h2>
<ul>
<li><a href="#安裝-python">第 1 步：安裝 Python</a></li>
<li><a href="#確認-python-環境">第 2 步：確認 Python 環境</a></li>
<li><a href="#準備專案檔案">第 3 步：準備專案檔案</a></li>
<li><a href="#安裝專案依賴">第 4 步：安裝專案依賴</a></li>
<li><a href="#執行打包指令">第 5 步：執行打包指令</a></li>
</ul>

<hr>

<h2 id="安裝-python">第 1 步：安裝 Python</h2>
<p>首先，您需要在電腦上安裝 Python。</p>
<ul>
<li>開啟您的瀏覽器，前往 Python 官方網站：<a href="https://www.python.org/downloads/" target="_blank">https://www.python.org/downloads/</a></li>
<li>
建議下載此版本 "<b>Download Python 3.12.10</b>"。
<blockquote><strong>注意</strong>: 使用此版本以上的 Python 可能會導致編譯錯誤。</blockquote>
</li>
<li>下載完成後，執行安裝檔。</li>
<li>
在安裝程式的歡迎畫面，請<b>務必勾選 "Add python.exe to PATH"</b>。這個選項非常重要，它能讓您在命令提示字元中直接使用 Python 指令。
</li>
<li>點擊 "Install Now"，等待安裝完成。</li>
</ul>

<hr>

<h2 id="確認-python-環境">第 2 步：確認 Python 環境</h2>
<p>安裝完成後，我們可以檢查一下 Python 是否已經安裝成功，以及 pip（Python 的套件管理工具）是否可用。</p>
<ul>
<li>按下鍵盤上的 <code>Win + R</code> 鍵，打開「執行」視窗。</li>
<li>輸入 <code>cmd</code>，然後按 Enter，打開命令提示字元。</li>
<li>在命令提示字元中，輸入以下指令並按 Enter：
<p><code>python --version</code></p>
如果螢幕上顯示類似 <code>Python 3.12.10</code> 這樣的版本號，代表 Python 已經安裝成功了。
</li>
<li>接著輸入以下指令並按 Enter，檢查 pip：
<p><code>pip --version</code></p>
如果顯示類似 <code>pip 25.0.1 from ...</code> 的資訊，表示 pip 也準備好了。
</li>
</ul>
<p><img src="https://i.postimg.cc/gjxNrNrG/2025-09-01-142635.png" alt="命令提示字元顯示 Python 與 pip 版本"></p>

<hr>

<h2 id="準備專案檔案">第 3 步：準備專案檔案</h2>
<p>現在，您需要將所有專案檔案放在同一個資料夾裡。</p>
<ul>
<li>在您的電腦上創建一個新資料夾，例如命名為 <code>Downloader Source code</code>。</li>
<li>將所有 Python 程式碼檔案（如 <code>main.py</code> 等）以及專案所需資源都放入此資料夾。</li>
</ul>

<hr>

<h2 id="安裝專案依賴">第 4 步：安裝專案依賴</h2>
<p>現在我們可以使用 pip 來安裝打包所需的套件了。</p>
<ul>
<li>在命令提示字元中，使用 <code>cd</code> 指令進入您剛才創建的 <code>Downloader Source code</code> 資料夾。
<p><code>cd &lt;您的資料夾路徑&gt;</code></p>
<blockquote>例如：<code>cd C:\Users\User\Desktop\Downloader Source code</code></blockquote>
</li>
<li>在該資料夾中，執行以下指令，安裝所有需要的套件：
<p><code>pip install -r requirements.txt</code></p>
</li>
<li>這個步驟會花一些時間，請耐心等待直到安裝完成。</li>
</ul>
<p><img src="https://i.postimg.cc/659CHHBq/2025-09-01-143052.png" alt="命令提示字元安裝依賴套件"></p>

<hr>

<h2 id="執行打包指令">第 5 步：執行打包指令</h2>
<p>所有準備工作都已完成，最後一步就是執行打包指令了。</p>
<ul>
<li>在同一個命令提示字元視窗中（確保路徑仍在您的專案資料夾內），複製並貼上以下指令（詳細指令請看<a href="https://github.com/kazusa777/kemonodownloader/blob/main/%E6%89%93%E5%8C%85%E6%8C%87%E4%BB%A4.txt" target="_blank">打包指令</a>）：
<pre><code>py -3.12 -m nuitka --mingw64 --onefile --windows-disable-console --enable-plugin=pyqt6 --windows-icon-from-ico="Bocchi 1.ico" --include-data-files="Bocchi 1.ico"="Bocchi 1.ico" --include-data-files=1.jpg=1.jpg --nofollow-import-to=tkinter,test,unittest,doctest,pydoc --include-module=downloader.downloader_concurrent --include-module=downloader.tasks --include-module=scraper.kemono --include-module=utils.file --include-module=utils.meta_dir --include-module=utils.update_status --remove-output --lto=yes --output-dir=build kazusa.py</code></pre>
</li>
<li>按 Enter 鍵執行。Nuitka 會開始編譯您的程式碼。</li>
<li>這個過程也會需要一段時間，請耐心等待。</li>
<li>當指令執行完畢，您會在專案資料夾中看到一個名為 <code>build</code> 的新資料夾。打開 <code>build</code> 資料夾，您就會看到一個名為 <code>kazusa.exe</code> 的可執行檔，這就是您打包好的軟體了。</li>
</ul>
<p><img src="https://i.postimg.cc/fT2S8DHq/2025-09-01-143149.png" alt="打包完成後產生的 exe 檔案"></p>
