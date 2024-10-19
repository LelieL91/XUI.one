<h1 align="center">XtreamUI.one</h1>

<p align="center">
  <a href="https://ko-fi.com/leliel91">
    <img src="https://ko-fi.com/img/githubbutton_sm.svg"
      alt="ko-fi"></a>
</p>

<h3 align="center">Install &amp; Update scripts for Debian OS (>= 11) based on latest XUI v1.5.13</h3>

---

### This is a work-in-progress repository made just for test and "forced" to work on Debian 12.
### MariaDB/MySQL server was removed to allow just a remote database connection.

---

## Run install/update script

- using curl: `bash <(curl -s 'https://raw.githubusercontent.com/LelieL91/XUI.one/main/install.sh')`
- using wget: `bash <(wget -q -O - 'https://raw.githubusercontent.com/LelieL91/XUI.one/main/install.sh')`

---

## Post Install/Current Issues
#### Debian 12 missing dependencies (XUI.one included PHP requirements): 
- [x] libjpeg8_8d-1+deb7u1_amd64
- [x] multiarch-support_2.28-10+deb10u4_amd64 (libssl pkg dep)
- [x] libssl1.1_1.1.1w-0+deb11u1_amd64
#### Default XUI.one Database Workaround (not all XUI.one tested):
- [ ] current_timestamp() sent as string: change these table column to NULL
<br>Tables: `lines`, `stream` - column: `updated`

---

### Credits ♥ [ [![](https://img.shields.io/badge/amidevous-%23121011.svg?style=for-the-badge?style=flat-square&logo=github&logoColor=white)](https://github.com/amidevous/xui.one) ] - [ [![](https://img.shields.io/badge/DRM_Scripts-%23121011.svg?style=for-the-badge?style=flat-square&logo=github&logoColor=white)](https://github.com/DRM-Scripts/XUI-One) ] - [ [![](https://img.shields.io/badge/emre1393-%23121011.svg?style=for-the-badge?style=flat-square&logo=github&logoColor=white)](https://github.com/emre1393/xtreamui_mirror) ] ♥

---
