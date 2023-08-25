- [OverView](#overview)
- [Step](#step)
  - [安装PVE](#安装PVE)
  - [获取root权限](#获取root权限)
- [生成授权文件](#生成授权文件)
  - [脚本](#脚本)
  - [配置port口](#配置port口)
  - [替换授权文件](#替换授权文件)
- [物理口映射](#物理口映射)
  - [检查BIOS设置](#检查BIOS设置)
  - [GRUB设置](#GRUB设置)
  - [Kernel Module设置](#Kernel Module设置)
  - [重启机器](#重启机器)
  - [校验](#校验)
  - [问题](#问题)
- [PVE物理口](#PVE物理口)
  - [加入vmbr0 + 映射进虚拟机](#加入vmbr0 + 映射进虚拟机)

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

### 配置port口
这里有两篇文章
[install fortigate in pve](https://getlabsdone.com/how-to-install-a-fortigate-firewall-on-proxmox/)
[Fortigate Administration Guide](https://docs.fortinet.com/document/fortigate-private-cloud/7.4.0/openstack-administration-guide/3275/setting-up-the-fortigate-vm-network-configuration)

可以跟着这个文章走一遍，就可以把port配好

### 替换授权文件
这一步需要先配置port1口的IP之后才能访问到web,访问之后会提示需不需要上传license文件。

## 物理口映射
[Arch Linux文档](https://wiki.archlinux.org/title/PCI_passthrough_via_OVMF)
[Proxmox文档](https://pve.proxmox.com/pve-docs/pve-admin-guide.html#qm_pci_passthrough)
### 检查BIOS设置
重启机器之后进入BIOS，一般配置都在CPU配置里面。不同的CPU配置选项不一样,像Intel的CPU就是VT-d，AMD的CPU就是AMD-Vi
要设置成Enabled，不能选Auto

### GRUB设置

打开`/etc/default/grub`文件之后修改：

```
GRUB_CMDLINE_LINUX="intel_iommu=on iommu=pt"
```

注意！！！
注意！！！
注意！！！

需要`update-grub`

### Kernel Module设置

打开 `/etc/modules`,添加

```
vfio
vfio_iommu_type1
vfio_pci
vfio_virqfd
```

最后再执行
```
update-initramfs -u -k all
```

### 重启机器
```
reboot
```

### 校验
```
dmesg | grep -i -e DMAR -e IOMMU
```
如果能看到`DMAR: IOMMU enabled`,那就说明好了


### 问题
Fortigate虚拟机里面不支持Intel 221网卡的驱动，所以这个直接映射没啥作用,还是只能把物理口先加进PVE然后在给到虚拟机

## PVE物理口
### 加入vmbr0 + 映射进虚拟机






