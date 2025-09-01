<h1>Kemono 下載器使用說明書與原始碼打包方法</h1>

<p align="center">
<strong><a href="#lang-zh-TW">繁體中文</a></strong>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
<strong><a href="#lang-zh-CN">简体中文</a></strong>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
<strong><a href="#lang-en">English</a></strong>
</p>

<hr>

<div id="lang-zh-TW">

<blockquote>
<p><strong>特別聲明與致謝</strong></p>
<p>本工具的原始版本由 Bilibili 創作者「<a href="https://www.bilibili.com/video/BV1TjKKztELJ/" target="_blank"><strong>比逗逗丶</strong></a>」所開發。因原版在本人電腦上無法使用，此版本是基於其在DC社群分享的原始碼修改而來，以供個人學習。本人僅為修改者，並非原始開發者。</p>
<p>本倉庫之內容，係為個人進行學術研究與資料探討而設立，其目的僅限於技術分析與學術交流，不涉及任何商業利益或非法活動之圖利。任何使用者不得將本倉庫之資料用於任何非法、不道德或具爭議性之行為，並應自行承擔所有因不當利用本平台資料所產生之法律責任與風險。</p>
</blockquote>

<h2>目錄</h2>
<ul>
<li><a href="#界面總覽">界面總覽</a></li>
<li><a href="#開始下載">開始下載</a></li>
<li><a href="#篩選貼文">篩選貼文</a></li>
<li><a href="#下載控制">下載控制</a></li>
<li><a href="#設定">設定</a></li>
<li><a href="#查看失敗項目">查看失敗項目</a></li>
<li><a href="#從原始碼打包"><strong style="color: #F38BA8;">從原始碼打包</strong></a></li>
<li><a href="#免責聲明">免責聲明</a></li>
</ul>

<hr>

<h2 id="界面總覽">界面總覽</h2>
<p><img src="https://i.postimg.cc/DZnD68PR/2025-09-01-160643.png" alt="Kemono 下載器主界面"></p>
<p>下載器的主界面由以下幾個部分構成：</p>
<ul>
<li><strong>主頁網址 (URL)</strong>: 輸入您想下載的創作者 Kemono 主頁連結。</li>
<li><strong>儲存路徑 (Path)</strong>: 選擇下載的檔案要儲存的本地資料夾位置。</li>
<li><strong>功能按鈕</strong>: 包含篩選貼文、開始下載、暫停、繼續、停止等操作。</li>
<li><strong>進度顯示</strong>: 顯示目前檔案的下載進度。</li>
<li><strong>執行日誌 (Log)</strong>: 顯示下載過程中的詳細資訊、進度與錯誤訊息。</li>
<li><strong>底部按鈕</strong>: 提供查看失敗項目與開啟設定的功能。</li>
</ul>

<hr>

<h2 id="開始下載">開始下載</h2>
<ol>
<li>在「主頁」欄位中，貼上創作者的 Kemono 主頁網址。</li>
<li>點擊「瀏覽...」按鈕，選擇您希望儲存檔案的資料夾。</li>
<li>點擊「開始下載」按鈕，程式將會開始下載該創作者的<strong>所有貼文與附件</strong>。</li>

</ol>
<hr>

<h2 id="篩選貼文">篩選貼文</h2>
<p>若您不想下載全部的貼文，可以使用此功能來選擇特定的貼文進行下載。</p>
<p><img src="https://i.postimg.cc/59LcJW6P/image.png" alt="篩選貼文界面"></p>
<ol>
<li>先填寫「主頁」網址。</li>
<li>點擊「篩選貼文」按鈕，程式會開啟一個新視窗並載入該創作者的所有貼文列表。</li>
<li>在列表中勾選您想要下載的貼文。</li>
<li>點擊「✅ 確認並開始下載」按鈕。</li>
<li>返回主介面後，再點擊「開始下載」，程式便只會下載您所選擇的貼文。</li>
</ol>
<blockquote><strong>注意</strong>：載入貼文列表可能需要一些時間，請耐心等候。</blockquote>

<hr>

<h2 id="下載控制">下載控制</h2>
<p>在下載過程中，您可以透過以下按鈕來控制下載任務：</p>
<ul>
<li><strong>暫停</strong>: 暫時停止下載任務。</li>
<li><strong>繼續</strong>: 從上次暫停的地方繼續下載。</li>
<li><strong>停止</strong>: 完全終止目前的下載任務。終止後無法繼續，需要重新開始。</li>
</ul>

<hr>

<h2 id="設定">設定</h2>
<p>點擊主界面右下角的「設定」按鈕，可以開啟設定視窗。您可以在此調整以下選項：</p>
<ul>
<li><strong>最大併發數 (Max Concurrency)</strong>: 設定同時下載的檔案數量。提高此數值可以加快下載速度，但也會增加網路與電腦的負擔。建議範圍為 1-50。</li>
<li><strong>日期命名模式 (Date Naming Mode)</strong>: 選擇是否要在檔案名稱中加入貼文的發布日期，以及日期的顯示位置（無、日期前綴、日期後綴）。</li>
</ul>

<hr>

<h2 id="查看失敗項目">查看失敗項目</h2>
<p>如果下載過程中有任何檔案下載失敗，您可以點擊主界面右下角的「查看失敗項目」按鈕。</p>
<p>這會開啟一個列表，顯示所有下載失敗的檔案路徑與原始連結。您可以點擊「複製全部」來複製這些資訊，以方便手動下載或進行問題排查。</p>

<hr style="border: 2px solid #45475a;">

<h2 id="從原始碼打包">從原始碼打包</h2>
<p>這是一份關於如何使用 Nuitka 將 Python 專案打包成獨立可執行檔 (.exe) 的簡易操作說明。本指南將引導您從安裝 Python 環境開始，到最終完成編譯。</p>

<h3>打包步驟目錄</h3>
<ul>
<li><a href="#第-1-步安裝-python">第 1 步：安裝 Python</a></li>
<li><a href="#第-2-步確認-python-環境">第 2 步：確認 Python 環境</a></li>
<li><a href="#第-3-步準備專案檔案">第 3 步：準備專案檔案</a></li>
<li><a href="#第-4-步安裝專案依賴">第 4 步：安裝專案依賴</a></li>
<li><a href="#第-5-步執行打包指令">第 5 步：執行打包指令</a></li>
</ul>

<hr>

<h3 id="第-1-步安裝-python">第 1 步：安裝 Python</h3>
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

<h3 id="第-2-步確認-python-環境">第 2 步：確認 Python 環境</h3>
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

<h3 id="第-3-步準備專案檔案">第 3 步：準備專案檔案</h3>
<p>現在，您需要將所有專案檔案放在同一個資料夾裡。</p>
<ul>
<li>在您的電腦上創建一個新資料夾，例如命名為 <code>Downloader Source code</code>。</li>
<li>將所有 Python 程式碼檔案（如 <code>main.py</code> 等）以及專案所需資源都放入此資料夾。</li>
</ul>

<hr>

<h3 id="第-4-步安裝專案依賴">第 4 步：安裝專案依賴</h3>
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

<h3 id="第-5-步執行打包指令">第 5 步：執行打包指令</h3>
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

<hr style="border: 2px solid #45475a;">

<h2 id="免責聲明">免責聲明 / Disclaimer</h2>
<h3>中文</h3>
<blockquote>
<p>本軟體僅供個人學習與技術研究使用，請勿用於任何商業或非法用途。</p>
<p>使用者透過本軟體下載之任何內容，其版權均歸原創作者所有。使用者應自行承擔因使用本軟體下載、儲存或散布受版權保護內容而可能引起之所有法律責任。</p>
<p>開發者不對任何因使用或無法使用本軟體所造成的直接或間接損害負責。使用者需自行承擔使用風險。</p>
<p>請尊重創作者的智慧財產權，並在下載和使用任何內容前，確保您已獲得合法授權。</p>
</blockquote>
<h3>English</h3>
<blockquote>
<p>This software is intended for personal educational and technical research purposes only. Do not use it for any commercial or illegal activities.</p>
<p>The copyright of any content downloaded by the user through this software belongs to the original creator. Users are solely responsible for all legal liabilities that may arise from downloading, storing, or distributing copyrighted content using this software.</p>
<p>The developer is not responsible for any direct or indirect damages caused by the use or inability to use this software. Users assume all risks associated with its use.</p>
<p>Please respect the intellectual property rights of creators and ensure you have obtained legal authorization before downloading and using any content.</p>
</blockquote>

</div>

<hr>

<details id="lang-zh-CN" open>
<summary><strong>简体中文</strong></summary>

<blockquote>
<p><strong>特别声明与致谢</strong></p>
<p>本工具的原始版本由 Bilibili 创作者「<a href="https://www.bilibili.com/video/BV1TjKKztELJ/" target="_blank"><strong>比逗逗丶</strong></a>」所开发。因原版在本人电脑上无法使用，此版本是基于其在DC社群分享的源代码修改而来，以供个人学习。本人仅为修改者，并非原始开发者。</p>
<p>本仓库之内容，系为个人进行学术研究与资料探讨而设立，其目的仅限于技术分析与学术交流，不涉及任何商业利益或非法活动之图利。任何使用者不得将本仓库之资料用于任何非法、不道德或具争议性之行为，并应自行承担所有因不当利用本平台资料所产生之法律责任与风险。</p>
</blockquote>

<h2>目录</h2>
<ul>
<li><a href="#界面总览-zh-cn">界面总览</a></li>
<li><a href="#开始下载-zh-cn">开始下载</a></li>
<li><a href="#筛选帖子-zh-cn">筛选帖子</a></li>
<li><a href="#下载控制-zh-cn">下载控制</a></li>
<li><a href="#设置-zh-cn">设置</a></li>
<li><a href="#查看失败项目-zh-cn">查看失败项目</a></li>
<li><a href="#从源代码打包-zh-cn"><strong style="color: #F38BA8;">从源代码打包</strong></a></li>
<li><a href="#免责声明-zh-cn">免责声明</a></li>
</ul>

<hr>

<h2 id="界面总览-zh-cn">界面总览</h2>
<p><img src="https://i.postimg.cc/DZnD68PR/2025-09-01-160643.png" alt="Kemono 下载器主界面"></p>
<p>下载器的主界面由以下几个部分构成：</p>
<ul>
<li><strong>主页网址 (URL)</strong>: 输入您想下载的创作者 Kemono 主页链接。</li>
<li><strong>存储路径 (Path)</strong>: 选择下载的文件要存储的本地文件夹位置。</li>
<li><strong>功能按钮</strong>: 包含筛选帖子、开始下载、暂停、继续、停止等操作。</li>
<li><strong>进度显示</strong>: 显示当前文件的下载进度。</li>
<li><strong>执行日志 (Log)</strong>: 显示下载过程中的详细信息、进度与错误信息。</li>
<li><strong>底部按钮</strong>: 提供查看失败项目与开启设置的功能。</li>
</ul>

<hr>

<h2 id="开始下载-zh-cn">开始下载</h2>
<ol>
<li>在“主页”栏位中，贴上创作者的 Kemono 主页网址。</li>
<li>点击“浏览...”按钮，选择您希望存储文件的文件夹。</li>
<li>点击“开始下载”按钮，程序将会开始下载该创作者的<strong style="color: #F38BA8;">所有帖子与附件</strong>。</li>
</ol>

<hr>

<h2 id="筛选帖子-zh-cn">筛选帖子</h2>
<p>若您不想下载全部的帖子，可以使用此功能来选择特定的帖子进行下载。</p>
<p><img src="https://i.postimg.cc/59LcJW6P/image.png" alt="筛选帖子界面"></p>
<ol>
<li>先填写“主页”网址。</li>
<li>点击“筛选帖子”按钮，程序会开启一个新窗口并加载该创作者的所有帖子列表。</li>
<li>在列表中勾选您想要下载的帖子。</li>
<li>点击“✅ 确认并开始下载”按钮。</li>
<li>返回主界面后，再点击“开始下载”，程序便只会下载您所选择的帖子。</li>
</ol>
<blockquote><strong>注意</strong>：加载帖子列表可能需要一些时间，请耐心等候。</blockquote>

<hr>

<h2 id="下载控制-zh-cn">下载控制</h2>
<p>在下载过程中，您可以通过以下按钮来控制下载任务：</p>
<ul>
<li><strong>暂停</strong>: 暂时停止下载任务。</li>
<li><strong>继续</strong>: 从上次暂停的地方继续下载。</li>
<li><strong>停止</strong>: 完全终止当前的下载任务。终止后无法继续，需要重新开始。</li>
</ul>

<hr>

<h2 id="设置-zh-cn">设置</h2>
<p>点击主界面右下角的“设置”按钮，可以开启设置窗口。您可以在此调整以下选项：</p>
<ul>
<li><strong>最大并发数 (Max Concurrency)</strong>: 设置同时下载的文件数量。提高此数值可以加快下载速度，但也会增加网络与电脑的负担。建议范围为 1-50。</li>
<li><strong>日期命名模式 (Date Naming Mode)</strong>: 选择是否要在文件名中加入帖子的发布日期，以及日期的显示位置（无、日期前缀、日期后缀）。</li>
</ul>

<hr>

<h2 id="查看失败项目-zh-cn">查看失败项目</h2>
<p>如果下载过程中有任何文件下载失败，您可以点击主界面右下角的“查看失败项目”按钮。</p>
<p>这会开启一个列表，显示所有下载失败的文件路径与原始链接。您可以点击“复制全部”来复制这些信息，以方便手动下载或进行问题排查。</p>

<hr style="border: 2px solid #45475a;">

<h2 id="从源代码打包-zh-cn">从源代码打包</h2>
<p>这是一份关于如何使用 Nuitka 将 Python 项目打包成独立可执行文件 (.exe) 的简易操作说明。本指南将引导您从安装 Python 环境开始，到最终完成编译。</p>

<h3>打包步骤目录</h3>
<ul>
<li><a href="#第-1-步安装-python-zh-cn">第 1 步：安装 Python</a></li>
<li><a href="#第-2-步确认-python-环境-zh-cn">第 2 步：确认 Python 环境</a></li>
<li><a href="#第-3-步准备项目文件-zh-cn">第 3 步：准备项目文件</a></li>
<li><a href="#第-4-步安装项目依赖-zh-cn">第 4 步：安装项目依赖</a></li>
<li><a href="#第-5-步执行打包指令-zh-cn">第 5 步：执行打包指令</a></li>
</ul>

<hr>

<h3 id="第-1-步安装-python-zh-cn">第 1 步：安装 Python</h3>
<p>首先，您需要在电脑上安装 Python。</p>
<ul>
<li>开启您的浏览器，前往 Python 官方网站：<a href="https://www.python.org/downloads/" target="_blank">https://www.python.org/downloads/</a></li>
<li>
建議下載此版本 "<b>Download Python 3.12.10</b>"。
<blockquote><strong>注意</strong>: 使用此版本以上的 Python 可能会导致编译错误。</blockquote>
</li>
<li>下载完成后，执行安装文件。</li>
<li>
在安装程序的欢迎界面，请<b>务必勾选 "Add python.exe to PATH"</b>。这个选项非常重要，它能让您在命令提示符中直接使用 Python 指令。
</li>
<li>点击 "Install Now"，等待安装完成。</li>
</ul>

<hr>

<h3 id="第-2-步确认-python-环境-zh-cn">第 2 步：确认 Python 环境</h3>
<p>安装完成后，我们可以检查一下 Python 是否已经安装成功，以及 pip（Python 的包管理工具）是否可用。</p>
<ul>
<li>按下键盘上的 <code>Win + R</code> 键，打开“运行”窗口。</li>
<li>输入 <code>cmd</code>，然后按 Enter，打开命令提示符。</li>
<li>在命令提示符中，输入以下指令并按 Enter：
<p><code>python --version</code></p>
如果屏幕上显示类似 <code>Python 3.12.10</code> 这样的版本号，代表 Python 已经安装成功了。</li>
<li>接着输入以下指令并按 Enter，检查 pip：
<p><code>pip --version</code></p>
如果显示类似 <code>pip 25.0.1 from ...</code> 的信息，表示 pip 也准备好了。</li>
</ul>
<p><img src="https://i.postimg.cc/gjxNrNrG/2025-09-01-142635.png" alt="命令提示符显示 Python 与 pip 版本"></p>

<hr>

<h3 id="第-3-步准备项目文件-zh-cn">第 3 步：准备项目文件</h3>
<p>现在，您需要将所有项目文件放在同一个文件夹里。</p>
<ul>
<li>在您的电脑上创建一个新文件夹，例如命名为 <code>Downloader Source code</code>。</li>
<li>将所有 Python 代码文件（如 <code>main.py</code> 等）以及项目所需资源都放入此文件夹。</li>
</ul>

<hr>

<h3 id="第-4-步安装项目依赖-zh-cn">第 4 步：安装项目依赖</h3>
<p>现在我们可以使用 pip 来安装打包所需的包了。</p>
<ul>
<li>在命令提示符中，使用 <code>cd</code> 指令进入您刚才创建的 <code>Downloader Source code</code> 文件夹。<p><code>cd &lt;您的文件夹路径&gt;</code></p><blockquote>例如：<code>cd C:\Users\User\Desktop\Downloader Source code</code></blockquote></li>
<li>在该文件夹中，执行以下指令，安装所有需要的包：<p><code>pip install -r requirements.txt</code></p></li>
<li>这个步骤会花一些时间，请耐心等待直到安装完成。</li>
</ul>
<p><img src="https://i.postimg.cc/659CHHBq/2025-09-01-143052.png" alt="命令提示符安装依赖包"></p>

<hr>

<h3 id="第-5-步执行打包指令-zh-cn">第 5 步：执行打包指令</h3>
<p>所有准备工作都已完成，最后一步就是执行打包指令了。</p>
<ul>
<li>在同一个命令提示符窗口中（确保路径仍在您的项目文件夹内），复制并贴上以下指令（详细指令请看<a href="https://github.com/kazusa777/kemonodownloader/blob/main/%E6%89%93%E5%8C%85%E6%8C%87%E4%BB%A4.txt" target="_blank">打包指令</a>）：<pre><code>py -3.12 -m nuitka --mingw64 --onefile --windows-disable-console --enable-plugin=pyqt6 --windows-icon-from-ico="Bocchi 1.ico" --include-data-files="Bocchi 1.ico"="Bocchi 1.ico" --include-data-files=1.jpg=1.jpg --nofollow-import-to=tkinter,test,unittest,doctest,pydoc --include-module=downloader.downloader_concurrent --include-module=downloader.tasks --include-module=scraper.kemono --include-module=utils.file --include-module=utils.meta_dir --include-module=utils.update_status --remove-output --lto=yes --output-dir=build kazusa.py</code></pre></li>
<li>按 Enter 键执行。 Nuitka 会开始编译您的代码。</li>
<li>这个过程也会需要一段时间，请耐心等待。</li>
<li>当指令执行完毕，您会在项目文件夹中看到一个名为 <code>build</code> 的新文件夹。打开 <code>build</code> 文件夹，您就会看到一个名为 <code>kazusa.exe</code> 的可执行文件，这就是您打包好的软件了。</li>
</ul>
<p><img src="https://i.postimg.cc/fT2S8DHq/2025-09-01-143149.png" alt="打包完成后产生的 exe 文件"></p>

<hr style="border: 2px solid #45475a;">

<h2 id="免責聲明-zh-cn">免责声明 / Disclaimer</h2>
<h3>中文</h3>
<blockquote>
<p>本软件仅供个人学习与技术研究使用，请勿用于任何商业或非法用途。</p>
<p>用户通过本软件下载之任何内容，其版权均归原创作者所有。用户应自行承担因使用本软件下载、存储或散布受版权保护内容而可能引起之所有法律责任。</p>
<p>开发者不对任何因使用或无法使用本软件所造成的直接或间接损害负责。用户需自行承担使用风险。</p>
<p>请尊重创作者的知识产权，并在下载和使用任何内容前，确保您已获得合法授权。</p>
</blockquote>
<h3>English</h3>
<blockquote>
<p>This software is intended for personal educational and technical research purposes only. Do not use it for any commercial or illegal activities.</p>
<p>The copyright of any content downloaded by the user through this software belongs to the original creator. Users are solely responsible for all legal liabilities that may arise from downloading, storing, or distributing copyrighted content using this software.</p>
<p>The developer is not responsible for any direct or indirect damages caused by the use or inability to use this software. Users assume all risks associated with its use.</p>
<p>Please respect the intellectual property rights of creators and ensure you have obtained legal authorization before downloading and using any content.</p>
</blockquote>

</details>

<hr>

<details id="lang-en" open>
<summary><strong>English</strong></summary>

<blockquote>
<p><strong>Special Statement &amp; Acknowledgements</strong></p>
<p>The original version of this tool was developed by the Bilibili creator "<a href="https://www.bilibili.com/video/BV1TjKKztELJ/" target="_blank"><strong>比逗逗丶</strong></a>". As the original version was not functional on my computer, this version is a modification based on the source code shared in their DC community for personal study. I am only a modifier, not the original developer.</p>
<p>The content of this repository is established for personal academic research and data exploration. Its purpose is strictly limited to technical analysis and academic exchange, and it does not involve any commercial interests or illegal activities. Users must not use the data from this repository for any illegal, unethical, or controversial purposes and shall bear all legal responsibilities and risks arising from the improper use of this platform's data.</p>
</blockquote>

<h2>Table of Contents</h2>
<ul>
<li><a href="#interface-overview-en">Interface Overview</a></li>
<li><a href="#start-download-en">Start Download</a></li>
<li><a href="#filter-posts-en">Filter Posts</a></li>
<li><a href="#download-control-en">Download Control</a></li>
<li><a href="#settings-en">Settings</a></li>
<li><a href="#view-failed-items-en">View Failed Items</a></li>
<li><a href="#build-from-source-code-en"><strong style="color: #F38BA8;">Build from Source Code</strong></a></li>
<li><a href="#disclaimer-en">Disclaimer</a></li>
</ul>

<hr>

<h2 id="interface-overview-en">Interface Overview</h2>
<p><img src="https://i.postimg.cc/DZnD68PR/2025-09-01-160643.png" alt="Kemono Downloader Main Interface"></p>
<p>The main interface of the downloader consists of the following parts:</p>
<ul>
<li><strong>Homepage URL</strong>: Enter the Kemono homepage link of the creator you want to download from.</li>
<li><strong>Save Path</strong>: Choose the local folder location where the downloaded files will be saved.</li>
<li><strong>Function Buttons</strong>: Includes operations like Filter Posts, Start Download, Pause, Resume, and Stop.</li>
<li><strong>Progress Display</strong>: Shows the download progress of the current file.</li>
<li><strong>Execution Log</strong>: Displays detailed information, progress, and error messages during the download process.</li>
<li><strong>Bottom Buttons</strong>: Provide functions to view failed items and open settings.</li>
</ul>

<hr>

<h2 id="start-download-en">Start Download</h2>
<ol>
<li>In the "Homepage" field, paste the creator's Kemono homepage URL.</li>
<li>Click the "Browse..." button to select the folder where you want to save the files.</li>
<li>Click the "Start Download" button, and the program will begin downloading <strong style="color: #F38BA8;">all posts and attachments</strong> from that creator.</li>
</ol>

<hr>

<h2 id="filter-posts-en">Filter Posts</h2>
<p>If you do not want to download all posts, you can use this function to select specific posts for download.</p>
<p><img src="https://i.postimg.cc/59LcJW6P/image.png" alt="Filter Posts Interface"></p>
<ol>
<li>First, fill in the "Homepage" URL.</li>
<li>Click the "Filter Posts" button. The program will open a new window and load a list of all posts by that creator.</li>
<li>Check the boxes for the posts you want to download from the list.</li>
<li>Click the "✅ Confirm and Start Download" button.</li>
<li>After returning to the main interface, click "Start Download" again, and the program will only download the posts you have selected.</li>
</ol>
<blockquote><strong>Note</strong>: Loading the post list may take some time. Please be patient.</blockquote>

<hr>

<h2 id="download-control-en">Download Control</h2>
<p>During the download process, you can control the task with the following buttons:</p>
<ul>
<li><strong>Pause</strong>: Temporarily stops the download task.</li>
<li><strong>Resume</strong>: Continues the download from where it was paused.</li>
<li><strong>Stop</strong>: Completely terminates the current download task. It cannot be resumed and must be started over.</li>
</ul>

<hr>

<h2 id="settings-en">Settings</h2>
<p>Click the "Settings" button in the bottom right corner of the main interface to open the settings window. You can adjust the following options here:</p>
<ul>
<li><strong>Max Concurrency</strong>: Sets the number of files to download simultaneously. Increasing this value can speed up downloads but also increases the load on your network and computer. A range of 1-50 is recommended.</li>
<li><strong>Date Naming Mode</strong>: Choose whether to include the post's publication date in the file name and where to place it (None, Date Prefix, Date Suffix).</li>
</ul>

<hr>

<h2 id="view-failed-items-en">View Failed Items</h2>
<p>If any files fail to download, you can click the "View Failed Items" button in the bottom right corner of the main interface.</p>
<p>This will open a list showing the paths and original links of all failed files. You can click "Copy All" to copy this information for manual download or troubleshooting.</p>

<hr style="border: 2px solid #45475a;">

<h2 id="build-from-source-code-en">Build from Source Code</h2>
<p>This is a simple guide on how to package a Python project into a standalone executable file (.exe) using Nuitka. This guide will walk you through from installing the Python environment to completing the final compilation.</p>

<h3>Build Steps Directory</h3>
<ul>
<li><a href="#step-1-install-python-en">Step 1: Install Python</a></li>
<li><a href="#step-2-verify-python-environment-en">Step 2: Verify Python Environment</a></li>
<li><a href="#step-3-prepare-project-files-en">Step 3: Prepare Project Files</a></li>
<li><a href="#step-4-install-project-dependencies-en">Step 4: Install Project Dependencies</a></li>
<li><a href="#step-5-execute-the-build-command-en">Step 5: Execute the Build Command</a></li>
</ul>

<hr>

<h3 id="step-1-install-python-en">Step 1: Install Python</h3>
<p>First, you need to install Python on your computer.</p>
<ul>
<li>Open your browser and go to the official Python website: <a href="https://www.python.org/downloads/" target="_blank">https://www.python.org/downloads/</a></li>
<li>
It is recommended to download this version: "<b>Download Python 3.12.10</b>".
<blockquote><strong>Note</strong>: Using a newer version of Python might cause compilation errors.</blockquote>
</li>
<li>After the download is complete, run the installer.</li>
<li>
On the welcome screen of the installer, <b>make sure to check "Add python.exe to PATH"</b>. This option is very important as it allows you to use Python commands directly in the command prompt.
</li>
<li>Click "Install Now" and wait for the installation to finish.</li>
</ul>

<hr>

<h3 id="step-2-verify-python-environment-en">Step 2: Verify Python Environment</h3>
<p>After installation, we can check if Python was installed successfully and if pip (Python's package manager) is available.</p>
<ul>
<li>Press <code>Win + R</code> on your keyboard to open the "Run" dialog.</li>
<li>Type <code>cmd</code> and press Enter to open the Command Prompt.</li>
<li>In the Command Prompt, type the following command and press Enter:<p><code>python --version</code></p>If it displays a version number like <code>Python 3.12.10</code>, Python is installed correctly.</li>
<li>Next, type the following command and press Enter to check pip:<p><code>pip --version</code></p>If it shows information like <code>pip 25.0.1 from ...</code>, pip is also ready.</li>
</ul>
<p><img src="https://i.postimg.cc/gjxNrNrG/2025-09-01-142635.png" alt="Command Prompt showing Python and pip versions"></p>

<hr>

<h3 id="step-3-prepare-project-files-en">Step 3: Prepare Project Files</h3>
<p>Now, you need to place all your project files into a single folder.</p>
<ul>
<li>Create a new folder on your computer, for example, name it <code>Downloader Source code</code>.</li>
<li>Place all Python code files (like <code>main.py</code>, etc.) and any necessary resources into this folder.</li>
</ul>

<hr>

<h3 id="step-4-install-project-dependencies-en">Step 4: Install Project Dependencies</h3>
<p>Now we can use pip to install the required packages for building.</p>
<ul>
<li>In the Command Prompt, use the <code>cd</code> command to navigate to the <code>Downloader Source code</code> folder you just created.<p><code>cd &lt;your_folder_path&gt;</code></p><blockquote>Example: <code>cd C:\Users\User\Desktop\Downloader Source code</code></blockquote></li>
<li>In that folder, run the following command to install all necessary packages:<p><code>pip install -r requirements.txt</code></p></li>
<li>This step will take some time. Please wait patiently for it to complete.</li>
</ul>
<p><img src="https://i.postimg.cc/659CHHBq/2025-09-01-143052.png" alt="Command Prompt installing dependencies"></p>

<hr>

<h3 id="step-5-execute-the-build-command-en">Step 5: Execute the Build Command</h3>
<p>With all preparations complete, the final step is to execute the build command.</p>
<ul>
<li>In the same Command Prompt window (make sure you are still in your project folder), copy and paste the following command (for the detailed command, see <a href="https://github.com/kazusa777/kemonodownloader/blob/main/%E6%89%93%E5%8C%85%E6%8C%87%E4%BB%A4.txt" target="_blank">Build Command</a>):<pre><code>py -3.12 -m nuitka --mingw64 --onefile --windows-disable-console --enable-plugin=pyqt6 --windows-icon-from-ico="Bocchi 1.ico" --include-data-files="Bocchi 1.ico"="Bocchi 1.ico" --include-data-files=1.jpg=1.jpg --nofollow-import-to=tkinter,test,unittest,doctest,pydoc --include-module=downloader.downloader_concurrent --include-module=downloader.tasks --include-module=scraper.kemono --include-module=utils.file --include-module=utils.meta_dir --include-module=utils.update_status --remove-output --lto=yes --output-dir=build kazusa.py</code></pre></li>
<li>Press Enter to execute. Nuitka will start compiling your code.</li>
<li>This process will also take some time. Please be patient.</li>
<li>Once the command finishes, you will see a new folder named <code>build</code> in your project directory. Open the <code>build</code> folder, and you will find an executable file named <code>kazusa.exe</code>, which is your packaged software.</li>
</ul>
<p><img src="https://i.postimg.cc/fT2S8DHq/2025-09-01-143149.png" alt="The exe file generated after build completion"></p>

<hr style="border: 2px solid #45475a;">

<h2 id="disclaimer-en">Disclaimer</h2>

<h3>English</h3>
<blockquote>
<p>This software is intended for personal educational and technical research purposes only. Do not use it for any commercial or illegal activities.</p>
<p>The copyright of any content downloaded by the user through this software belongs to the original creator. Users are solely responsible for all legal liabilities that may arise from downloading, storing, or distributing copyrighted content using this software.</p>
<p>The developer is not responsible for any direct or indirect damages caused by the use or inability to use this software. Users assume all risks associated with its use.</p>
<p>Please respect the intellectual property rights of creators and ensure you have obtained legal authorization before downloading and using any content.</p>
</blockquote>

</details>
