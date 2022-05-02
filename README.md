# FileManager Helper

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/ico.png">

## Welcome to FileManager

<p>
<a href = "https://github.com/YubaC/filemanager"><img src = "https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a>

<img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white">

<img src = "https://img.shields.io/badge/Windows_XP-003399?style=for-the-badge&logo=windows-xp&logoColor=white">
</p>

<p>
<a target="_blank" href="https://github.com/YubaC/filemanager"><img id="watchers" src="https://img.shields.io/github/watchers/YubaC/filemanager.svg?style=for-the-badge&color=green"></a>
<a target="_blank" href="https://github.com/YubaC/filemanager"><img id="forks" src="https://img.shields.io/github/forks/YubaC/filemanager.svg?style=for-the-badge&color=green"></a>
<a target="_blank" href="https://github.com/YubaC/filemanager"><img id="stars" src="https://img.shields.io/github/stars/YubaC/filemanager.svg?style=for-the-badge&color=green"></a>
</p>

<p>
<a target="_blank" href="https://github.com/YubaC/filemanager/releases"><img src="https://img.shields.io/github/v/release/YubaC/filemanager?style=for-the-badge&color=yellowgreen"></a> <img id="download_times" src="https://img.shields.io/github/downloads/YubaC/filemanager/total?style=for-the-badge&color=yellow"> <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/github/pipenv/locked/python-version/YubaC/filemanager?style=for-the-badge&color=orange"></a>
</p>
<p><img src="https://img.shields.io/badge/AUTHOR-YubaC-orange?style=for-the-badge&color=red"> <img src="https://img.shields.io/badge/DOCUMENT%20VERSION-1.0.1-orange?style=for-the-badge&color=blueviolet"></p><p>

<img src="http://ForTheBadge.com/images/badges/made-with-python.svg">

<img src = "http://ForTheBadge.com/images/badges/built-with-science.svg">

<br>

<img src = "http://ForTheBadge.com/images/badges/built-by-developers.svg">

<img src = "http://ForTheBadge.com/images/badges/built-with-love.svg">
</p>

**FileManager**是一款轻量的文件管理器。

### 安装 FileManger

双击`install.bat`以执行安装。

访问[https://github.com/YubaC/filemanager/releases](https://github.com/YubaC/filemanager/releases)以获取最新版。

### 升级 FileManager

FileManager 每次启动时都会启动一个 update checker。

- 如果没有更新，updater checker 会自行退出。
- 如果存在更新，您可以通过输入`y`或`N`（不区分大小写）的方式来决定是否进行更新。

**请注意！更新有可能失败。当 updater 的下载进度条长时间不变化时，请尝试关闭 updater 并重新进行更新。**

## Quick Start

**使用`help`命令以获取帮助，使用'help -?'命令以打开此文档。**

### 启动 FileManager

在正确安装 FileManager 后，当在文件夹下右键时，弹出的右键菜单应会包含“在这里打开 FileManager”的选项。

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/open_in_there.png" alt = "在这里打开FileManager.png">

### 认识 FileManager 界面

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/fm_window.png" alt = "fm_window.png">

①：当前版本

②：工作路径

③：命令输入

**除去在$处单击鼠标外，双击窗口或按 tab 键以快速聚焦。**

**在输入时使用键盘的 ↑↓ 键以快速调出历史命令，按 F7 以打开历史命令记录。在历史命令记录里选中的命令可以使用回车快速输入。**

### 新建仓库

使用`cd`以更改工作目录。

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/cd_dir.png">

除了使用相对路径外，`cd`命令同样也支持绝对路径。列如：

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/cd_dir2.png">

**目标路径存在空格时，请使用**`cd,路径`**的方式更改工作目录。**
列如：

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/cd_dir3.png">

**请注意！所用逗号必须为半角符号（英文符号）。**

在命令行输入`init newrepo`以在工作路径处新建一个仓库。

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/init_newrepo.png">

这是新建仓库前的 FMTest 文件夹：

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/before_init_newrepo.png">

可以看到，新建仓库后，仓库所在文件夹下多出了一个隐藏的.filemanager 文件夹。

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/after_init_newrepo.png">

### 加载仓库

使用`init`以加载工作路径下的仓库。

当出现这样的提示时，使用`init -update`以将仓库提升至当前版本：

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/init_error.png">

加载成功后如下：

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/init.png">

可以看到，在工作路径下多出了一个括号和六位数字/字母。这是该仓库的 id。
**这是加载成功的标志。**

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/branch_in_init.png">

红框内是该仓库的分支图。详情请参阅<a href = "#branches">分支</a>

### 检测仓库内文件的更新

#### refreash

`refreash`命令可以刷新整个仓库，检测所有更改，但耗时较长。

#### reload

`reload`命令可以刷新整个仓库，检测所有更改，耗时较短，但需要 monitor 的支持。
关于开启/关闭 monitor 的监控，详情请参阅<a href = "#set">仓库设置</a>

#### 更改/删除/新建的文件

加载后，如果没有更改，将会提示“没有最近更改的文件”：

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/no_new.png">

否则将会弹窗提示更改的文件。这里我们新建一个 4.txt：

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/change_box.png">

可以看到，弹出了一个名为“ChangesList”的弹窗。

“ChangesList”弹窗分上下两个 ListBox。上部是所有更改/删除/新建的文件列表，下部是暂存的文件列表。

在下部选中的文件可以通过“删除”按钮移除。在上部选中的文件可以通过“添加”按钮暂存。

除此之外，还可以使用`add`命令进行暂存操作。详情请参阅<a href = "#add">添加/移除暂存的文件</a>

**请注意！所有的空文件夹都不会被算在内。**

<span id = "add"></span>

### 添加/移除暂存的文件

在刷新仓库并确认有更改/删除/新建的文件后，可以使用`add`命令以添加/移除暂存的文件。

- 使用`add`命令以唤起添加/移除文件(文件夹)面板：

  <img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/add.png">

  <img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/adder.png">

  将文件或文件夹拖拽到该面板上以将其暂存/取消暂存。

- 使用`add -f +`和`add -f -`以暂存/取消暂存文件。
- 使用`add -d +`和`add -d -`以暂存/取消暂存文件夹及其子文件。

**请注意！以上两个命令将会弹出如下图所示的一个文件选择框。**

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/file_selector.png">

**add 后的附加参数(-f/-d/+/-)排序不分先后。因此，命令`add -f/-d +/-`和`add +/- -f/-d`是完全等效的。**

### 提交暂存的文件

`commit`命令可以提交暂存的文件。方法是：`commit '提交注释'`或`commit "提交注释"`。两种方法完全等效。

**请注意！所用引号必须为半角符号（英文符号）。**

例：提交注释为“My first commit”：

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/commit.png">

**如果所在的提交不是当前分支的最后一个提交的话，会新建一个分支。**

例如：

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/branch3.png">

表示在 id=0 的提交处又进行了一次提交。

关于分支，请参阅<a href = "#branches">分支</a>

<span id = "checkout"></span>

### 检出文件

`checkout`命令可以检出选中的提交，即将仓库恢复至所选中的提交提交时的状态。

方法是：`checkout 提交id`，列如：

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/checkout.png">

上图表示将仓库恢复至 id=0 的提交（新建仓库）时。

<span id = "branches"></span>

### 分支

`branch`命令可以显示当前仓库的分支图。例如：

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/branch1.png">

又或者：

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/branch2.png">

分支图上的每一个星号（\*）表示一次提交。竖线表示分支。

对应星号右侧是该次提交的提交说明。括号内的 id(id=x)为该次提交的编号。

星号右下侧的加号和横线/反斜杠（\）表示从该提交延伸出的子分支。列如，上图中的 id=8~10 的提交表示在 id=1 的提交处又进行了一次提交（id=8），并且在这个提交（id=8）的基础上又提交了 id=9 和 id=10 的提交。

又如：

<img src = "https://cdn.jsdelivr.net/gh/YubaC/fmhelp@latest/img/branch3.png">

其含义为：在 id=0 的提交（新建仓库）出，引出一个子分支（id=2）。

### 比较文件的不同

`diff`命令可以比较文件的不同。

- 当没有加载仓库时，diff 将会要求选择两个不同的文件以进行对比。
- 当加载了仓库时，diff 将会要求打开一个文件，并试图在其所处分支里寻找并比较其与上一次提交时的差异。

如果想保存比较所生成的对比文件(一个 html 网页)，请使用`diff -s`。

无论是否选择保存，diff 都将会在比较完成后用浏览器打开对比文件。

**请注意！`diff`命令只能比较文本文件，形如.word,.ppt,.xls,.psd 等二进制文件均不在可比较的范围内。**

<span id = "set"></span>

### 仓库设置

#### monitor

- 使用`set monitor on`以为当前仓库启用 monitor。
- 使用`set monitor off`以为当前仓库禁用 monitor。

> 什么时候适合启用 monitor?<br>
> 当一个仓库内文件特别多的时候，refreash 会花费很长时间，这时适合启用 monitor，可以大量节省 refreash 的时间。如果 refreash 耗时很短，则不建议启用 monitor。
