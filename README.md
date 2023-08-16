- [OverView](#overview)
- [Step](#step)
  - [安装PVE](#安装PVE)
  - [获取root权限](#获取root权限)
- [生成授权文件](#生成授权文件)
  - [脚本](#脚本)
  - [替换授权文件](#替换授权文件)
  - [启动](#启动)

# OverView
软路由里面装PVE之后，需要把FortiGate虚拟机导入，并且获取FortiGate的root权限跟License

# Step
## 安装PVE
1. [下载镜像](https://www.proxmox.com/en/downloads)
2. [下载Ventoy](https://github.com/ventoy/Ventoy)
3. 把Proxmox镜像通过Ventoy烧进U盘之后，最好先插上U盘之后再给软路由工控机通电，有些机器一通电就启动了，关机键都没用，离谱。
4. 正常安装PVE，要设置一些网络，最好就静态配置一下IP，配到当前的内网。
5. 安装好之后，需要从硬路由再牵一根线插到软路由机器上面，这样从Windows这边的浏览器才能访问到第四步配置的IP地址,举个例子: `https://192.168.199.111:8006/`


## 获取FortiGate root权限
### 编译BusyBox
### 修改FortiGate /bin/init文件


## 生成授权文件
### 脚本
借用大佬的[脚本](https://github.com/rrrrrrri/fos-license-gen/blob/main/gen_lic.py)，我们能直接生成我们自己的license文件

### 替换授权文件
导入到镜像里面之后，再把镜像放到PVE里

### 启动
