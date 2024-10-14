#!/usr/bin/python3
import subprocess, os, random, string, sys, shutil, socket, time, io

if sys.version_info.major != 3:
    print("Please run with python3.")
    sys.exit(1)

rPath = os.path.dirname(os.path.realpath(__file__))
rPackages = ["cpufrequtils", "iproute2", "net-tools", "dirmngr", "gpg-agent", "libmaxminddb0", "libmaxminddb-dev", "mmdb-bin", "libcurl4", "libgeoip-dev", "libxslt1-dev", "libonig-dev", "e2fsprogs", "wget", "mariadb-client", "sysstat", "alsa-utils", "v4l-utils", "mcrypt", "certbot", "iptables-persistent", "libjpeg-dev", "libpng-dev", "php-ssh2", "xz-utils", "zip", "unzip"]
rRemove = ["mysql-server"]
#rMySQLCnf = '# XUI\n[client]\nport                            = 3306\n\n[mysqld_safe]\nnice                            = 0\n\n[mysqld]\nuser                            = mysql\nport                            = 3306\nbasedir                         = /usr\ndatadir                         = /var/lib/mysql\ntmpdir                          = /tmp\nlc-messages-dir                 = /usr/share/mysql\nskip-external-locking\nskip-name-resolve\nbind-address                    = *\n\nkey_buffer_size                 = 128M\nmyisam_sort_buffer_size         = 4M\nmax_allowed_packet              = 64M\nmyisam-recover-options          = BACKUP\nmax_length_for_sort_data        = 8192\nquery_cache_limit               = 0\nquery_cache_size                = 0\nquery_cache_type                = 0\nexpire_logs_days                = 10\nmax_binlog_size                 = 100M\nmax_connections                 = 8192\nback_log                        = 4096\nopen_files_limit                = 20240\ninnodb_open_files               = 20240\nmax_connect_errors              = 3072\ntable_open_cache                = 4096\ntable_definition_cache          = 4096\ntmp_table_size                  = 1G\nmax_heap_table_size             = 1G\n\ninnodb_buffer_pool_size         = 10G\ninnodb_buffer_pool_instances    = 10\ninnodb_read_io_threads          = 64\ninnodb_write_io_threads         = 64\ninnodb_thread_concurrency       = 0\ninnodb_flush_log_at_trx_commit  = 0\ninnodb_flush_method             = O_DIRECT\nperformance_schema              = 0\ninnodb-file-per-table           = 1\ninnodb_io_capacity              = 20000\ninnodb_table_locks              = 0\ninnodb_lock_wait_timeout        = 0\n\nsql_mode                        = "NO_ENGINE_SUBSTITUTION"\n\n[mariadb]\n\nthread_cache_size               = 8192\nthread_handling                 = pool-of-threads\nthread_pool_size                = 12\nthread_pool_idle_timeout        = 20\nthread_pool_max_threads         = 1024\n\n[mysqldump]\nquick\nquote-names\nmax_allowed_packet              = 16M\n\n[mysql]\n\n[isamchk]\nkey_buffer_size                 = 16M'
#rConfig = '; XUI Configuration\n; -----------------\n; Your username and password will be encrypted and\n; saved to the \'credentials\' file in this folder\n; automatically.\n;\n; To change your username or password, modify BOTH\n; below and XUI will read and re-encrypt them.\n\n[XUI]\nhostname    =   "127.0.0.1"\ndatabase    =   "xui"\nport        =   3306\nserver_id   =   1\nlicense     =   ""\n\n[Encrypted]\nusername    =   "%s"\npassword    =   "%s"'
rConfig='; XUI Configuration\n; -----------------\n; Your username and password will be encrypted and\n; saved to the \'credentials\' file in this folder\n; automatically.\n;\n; To change your username or password, modify BOTH\n; below and XUI will read and re-encrypt them.\n\n[XUI]\nhostname    =   "%s"\ndatabase    =   "%s"\nport        =   %s\nserver_id   =   1\nlicense     =   ""\n\n[Encrypted]\nusername    =   "%s"\npassword    =   "%s"'
rRedisConfig = "bind *\nprotected-mode yes\nport 6379\ntcp-backlog 511\ntimeout 0\ntcp-keepalive 300\ndaemonize yes\nsupervised no\npidfile /home/xui/bin/redis/redis-server.pid\nloglevel warning\nlogfile /home/xui/bin/redis/redis-server.log\ndatabases 1\nalways-show-logo yes\nstop-writes-on-bgsave-error no\nrdbcompression no\nrdbchecksum no\ndbfilename dump.rdb\ndir /home/xui/bin/redis/\nslave-serve-stale-data yes\nslave-read-only yes\nrepl-diskless-sync no\nrepl-diskless-sync-delay 5\nrepl-disable-tcp-nodelay no\nslave-priority 100\nrequirepass #PASSWORD#\nmaxclients 655350\nlazyfree-lazy-eviction no\nlazyfree-lazy-expire no\nlazyfree-lazy-server-del no\nslave-lazy-flush no\nappendonly no\nappendfilename \"appendonly.aof\"\nappendfsync everysec\nno-appendfsync-on-rewrite no\nauto-aof-rewrite-percentage 100\nauto-aof-rewrite-min-size 64mb\naof-load-truncated yes\naof-use-rdb-preamble no\nlua-time-limit 5000\nslowlog-log-slower-than 10000\nslowlog-max-len 128\nlatency-monitor-threshold 0\nnotify-keyspace-events \"\"\nhash-max-ziplist-entries 512\nhash-max-ziplist-value 64\nlist-max-ziplist-size -2\nlist-compress-depth 0\nset-max-intset-entries 512\nzset-max-ziplist-entries 128\nzset-max-ziplist-value 64\nhll-sparse-max-bytes 3000\nactiverehashing yes\nclient-output-buffer-limit normal 0 0 0\nclient-output-buffer-limit slave 256mb 64mb 60\nclient-output-buffer-limit pubsub 32mb 8mb 60\nhz 10\naof-rewrite-incremental-fsync yes\nsave 60 1000\nserver-threads 4\nserver-thread-affinity true"
rSysCtl = '# XUI.one\n\nnet.ipv4.tcp_congestion_control = bbr\nnet.core.default_qdisc = fq\nnet.ipv4.tcp_rmem = 8192 87380 134217728\nnet.ipv4.udp_rmem_min = 16384\nnet.core.rmem_default = 262144\nnet.core.rmem_max = 268435456\nnet.ipv4.tcp_wmem = 8192 65536 134217728\nnet.ipv4.udp_wmem_min = 16384\nnet.core.wmem_default = 262144\nnet.core.wmem_max = 268435456\nnet.core.somaxconn = 1000000\nnet.core.netdev_max_backlog = 250000\nnet.core.optmem_max = 65535\nnet.ipv4.tcp_max_tw_buckets = 1440000\nnet.ipv4.tcp_max_orphans = 16384\nnet.ipv4.ip_local_port_range = 2000 65000\nnet.ipv4.tcp_no_metrics_save = 1\nnet.ipv4.tcp_slow_start_after_idle = 0\nnet.ipv4.tcp_fin_timeout = 15\nnet.ipv4.tcp_keepalive_time = 300\nnet.ipv4.tcp_keepalive_probes = 5\nnet.ipv4.tcp_keepalive_intvl = 15\nfs.file-max=20970800\nfs.nr_open=20970800\nfs.aio-max-nr=20970800\nnet.ipv4.tcp_timestamps = 1\nnet.ipv4.tcp_window_scaling = 1\nnet.ipv4.tcp_mtu_probing = 1\nnet.ipv4.route.flush = 1\nnet.ipv6.route.flush = 1'
rSystemd = '[Unit]\nSourcePath=/home/xui/service\nDescription=XUI.one Service\nAfter=network.target\nStartLimitIntervalSec=0\n\n[Service]\nType=simple\nUser=root\nRestart=always\nRestartSec=1\nExecStart=/bin/bash /home/xui/service start\nExecRestart=/bin/bash /home/xui/service restart\nExecStop=/bin/bash /home/xui/service stop\n\n[Install]\nWantedBy=multi-user.target'
rChoice = "23456789abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ"

rVersions = {
    "11": "bullseye",
    "12": "bookworm"
}

class col:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def generate(length=32): return ''.join(random.choice(rChoice) for i in range(length))

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def printc(rText, rColour=col.OKBLUE, rPadding=0):
    rLeft = int(30-(len(rText)/2))
    rRight = (60-rLeft-len(rText))
    print("%s |--------------------------------------------------------------| %s" % (rColour, col.ENDC))
    for i in range(rPadding): print ("%s |                                                              | %s" % (rColour, col.ENDC))
    print("%s | %s%s%s | %s" % (rColour, " " * rLeft, rText, " " * rRight, col.ENDC))
    for i in range(rPadding): print ("%s |                                                              | %s" % (rColour, col.ENDC))
    print("%s |--------------------------------------------------------------| %s" % (rColour, col.ENDC))
    print(" ")

if __name__ == "__main__":
    ##################################################
    # START                                          #
    ##################################################
    
    try: rVersion = os.popen('lsb_release -sr').read().strip()
    except: rVersion = None
    if not rVersion in rVersions:
        printc("Unsupported Operating System")
        sys.exit(1)
    
    if not os.path.exists("/root/xui.tar.gz") and not os.path.exists("/root/xui_trial.tar.gz"):
        print("Fatal Error: xui.tar.gz is missing. Please download it from XUI billing panel.")
        sys.exit(1)
    
    printc("XUI", col.OKGREEN, 2)
    #rHost = "127.0.0.1" ; rServerID = 1 ; rUsername = generate() ; rPassword = generate()
    #rDatabase = "xui"
    #rPort = 3306
    rHost = input("Enter DB Host: ")
    rPort = input("Enter DB Port: ")
    rDatabase = input("Enter DB Name: ")
    rUsername = input("Enter DB Username: ")
    rPassword = input("Enter DB Password: ")

    if os.path.exists("/home/xui/"):
        printc("XUI Directory Exists!")
        while True:
            rAnswer = input("Continue and overwrite? (Y / N) : ")
            if rAnswer.upper() in ["Y", "N"]: break
        if rAnswer == "N": sys.exit(1)
   
    ##################################################
    # UPGRADE                                        #
    ##################################################
    
    printc("Preparing Installation")
    for rFile in ["/var/lib/dpkg/lock-frontend", "/var/cache/apt/archives/lock", "/var/lib/dpkg/lock", "/var/lib/apt/lists/lock"]:
        if os.path.exists(rFile):
            try: os.remove(rFile)
            except: pass
    printc("Updating system")
    os.system("sudo DEBIAN_FRONTEND=noninteractive apt-get update >/dev/null 2>&1")
    for rPackage in rRemove:
        printc("Removing %s" % rPackage)
        os.system("sudo DEBIAN_FRONTEND=noninteractive apt-get remove %s -y >/dev/null 2>&1" % rPackage)
    for rPackage in rPackages:
        printc("Installing %s" % rPackage)
        os.system("sudo DEBIAN_FRONTEND=noninteractive apt-get -yq install %s >/dev/null 2>&1" % rPackage)
    try: subprocess.check_output("getent passwd xui".split())
    except:
        printc("Creating user")
#        os.system("sudo adduser --system --shell /bin/false --group --disabled-login xui >/dev/null 2>&1")
        os.system("sudo adduser --system --shell /bin/false xui >/dev/null 2>&1")
    if not os.path.exists("/home/xui >/dev/null 2>&1"): os.mkdir("/home/xui")
    
    ##################################################
    # INSTALL                                        #
    ##################################################
    
    printc("Installing XUI")
    if os.path.exists("/root/xui.tar.gz"):
        os.system('sudo tar -xzf "/root/xui.tar.gz" -C "/home/xui/"')
        if not os.path.exists("/home/xui/status"):
            printc("Failed to extract! Exiting")
            sys.exit(1)
    elif os.path.exists("/rootxui_trial.tar.gz"):
        os.system('sudo tar -xzf "/rootxui_trial.tar.gz" -C "/home/xui/"')
        if not os.path.exists("/home/xui/status"):
            printc("Failed to extract! Exiting")
            sys.exit(1)
    
    ##################################################
    # MYSQL                                          #
    ##################################################
    
    printc("Configuring MySQL")
    rRet = os.system('sudo mysql -u "%s" -p"%s" -h "%s" -P %s -D "%s" -e \"SELECT VERSION();\"' % (rUsername, rPassword, rHost, rPort, rDatabase))
    if rRet != 0:
        while True:
            printc("Invalid Database credentials! Please try again.")
            rHost = input("Enter DB Host: ")
            rPort = input("Enter DB Port: ")
            rDatabase = input("Enter DB Name: ")
            rUsername = input("Enter DB Username: ")
            rPassword = input("Enter DB Password: ")
            rRet = os.system('mysql -u "%s" -p"%s" -h "%s" -P %s -D "%s" -e \"SELECT VERSION();\" >/dev/null 2>&1' % (rUsername, rPassword, rHost, rPort, rDatabase))
            if rRet == 0: break
    os.system('sudo mysql -u "%s" -p"%s" -h "%s" -P %s %s < "/home/xui/bin/install/database.sql"' % (rUsername, rPassword, rHost, rPort, rDatabase))
    rConfigData = rConfig % (rHost, rDatabase, rPort, rUsername, rPassword)
    rFile = io.open("/home/xui/config/config.ini", "w", encoding="utf-8")
    rFile.write(rConfigData)
    rFile.close()

    ##################################################
    # CONFIGURE                                      #
    ##################################################
    
    printc("Configuring System")
    if not "/home/xui/" in open("/etc/fstab").read():
        rFile = io.open("/etc/fstab", "a", encoding="utf-8")
        rFile.write("\ntmpfs /home/xui/content/streams tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=90% 0 0\ntmpfs /home/xui/tmp tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=6G 0 0")
        rFile.close()
    if os.path.exists("/etc/init.d/xuione"): os.remove("/etc/init.d/xuione")
    if os.path.exists("/etc/systemd/system/xui.service"): os.remove("/etc/systemd/system/xui.service")
    if not os.path.exists("/etc/systemd/system/xuione.service"):
        rFile = io.open("/etc/systemd/system/xuione.service", "w", encoding="utf-8")
        rFile.write(rSystemd)
        rFile.close()
        os.system("sudo chmod +x /etc/systemd/system/xuione.service >/dev/null 2>&1")
        os.system("sudo systemctl daemon-reload >/dev/null 2>&1")
        os.system("sudo systemctl enable xuione >/dev/null 2>&1")
    print("Custom sysctl.conf - If you have your own custom sysctl.conf, type N or it will be overwritten. If you don't know what a sysctl configuration is, type Y as it will correctly set your TCP settings and open file limits.")
    print(" ")
    while True:
        rAnswer = input("Overwrite sysctl configuration? Recommended! (Y / N): ")
        if rAnswer.upper() in ["Y", "N"]: break
    if rAnswer.upper() == "Y":
        try: os.system("sudo modprobe ip_conntrack >/dev/null 2>&1")
        except: pass
        try:
            rFile = io.open("/etc/sysctl.conf", "w", encoding="utf-8")
            rFile.write(rSysCtl)
            rFile.close()
            os.system("sudo sysctl -p >/dev/null 2>&1")
            rFile = open("/home/xui/config/sysctl.on", "w")
            rFile.close()
        except: print("Failed to write to sysctl file.")
    else:
        if os.path.exists("/home/xui/config/sysctl.on"): os.remove("/home/xui/config/sysctl.on")
    if not "DefaultLimitNOFILE=655350" in open("/etc/systemd/system.conf").read():
        os.system("sudo echo \"\nDefaultLimitNOFILE=655350\" >> \"/etc/systemd/system.conf\"")
        os.system("sudo echo \"\nDefaultLimitNOFILE=655350\" >> \"/etc/systemd/user.conf\"")
    if not os.path.exists("/home/xui/bin/redis/redis.conf"):
        rFile = io.open("/home/xui/bin/redis/redis.conf", "w", encoding="utf-8")
        rFile.write(rRedisConfig)
        rFile.close()
    
    ##################################################
    # ACCESS CODE                                    #
    ##################################################
    
    rCodeDir = "/home/xui/bin/nginx/conf/codes/"
    rHasAdmin = None
    for rCode in os.listdir(rCodeDir):
        if rCode.endswith(".conf"):
            if rCode.split(".")[0] == "setup": os.remove(rCodeDir + "setup.conf")
            elif "/home/xui/admin" in open(rCodeDir + rCode, "r").read(): rHasAdmin = rCode
    if not rHasAdmin:
        rCode = generate(8)
        os.system('sudo mysql -u "%s" -p"%s" -h "%s" -P %s -D "%s" -e "INSERT INTO access_codes(code, type, enabled, groups) VALUES(\'%s\', 0, 1, \'[1]\');"' % (rUsername, rPassword, rHost, rPort, rDatabase, rCode))
        rTemplate = open(rCodeDir + "template").read()
        rTemplate = rTemplate.replace("#WHITELIST#", "")
        rTemplate = rTemplate.replace("#TYPE#", "admin")
        rTemplate = rTemplate.replace("#CODE#", rCode)
        rTemplate = rTemplate.replace("#BURST#", "500")
        rFile = io.open("%s%s.conf" % (rCodeDir, rCode), "w", encoding="utf-8")
        rFile.write(rTemplate)
        rFile.close()
    else: rCode = rHasAdmin.split(".")[0]
    
    ##################################################
    # FINISHED                                       #
    ##################################################
    
    os.system("sudo mount -a >/dev/null 2>&1")
    os.system("sudo chown -R xui:xui '/home/xui' >/dev/null 2>&1")
    os.system("sudo systemctl daemon-reload >/dev/null 2>&1")
    os.system("sudo systemctl start xuione >/dev/null 2>&1")
    
    time.sleep(10)
    os.system("sudo /home/xui/status 1 >/dev/null 2>&1")
    # License patch section start
    time.sleep(10)
    os.system("sudo wget https://github.com/LelieL91/XUI.one/releases/download/1.5.13/xui_crack.tar.gz -qO /root/xui_crack.tar.gz >/dev/null 2>&1")
    os.system("sudo tar -xf /root/xui_crack.tar.gz")
    os.system("sudo systemctl stop xuione >/dev/null 2>&1")
    os.system("sudo cp -r license /home/xui/config/license >/dev/null 2>&1")
    os.system("sudo cp -r xui.so /home/xui/bin/php/lib/php/extensions/no-debug-non-zts-20190902/xui.so >/dev/null 2>&1")
    os.system('sudo sed -i "s/^license.*/license     =   \"cracked\"/g" /home/xui/config/config.ini >/dev/null 2>&1')
    os.system("sudo systemctl start xuione >/dev/null 2>&1")
    # License path section end
    os.system("sudo /home/xui/bin/php/bin/php /home/xui/includes/cli/startup.php >/dev/null 2>&1")
    
    rFile = io.open(rPath + "/credentials.txt", "w", encoding="utf-8")
    rFile.write("MariaDB Host: %s:%s" % (rHost, rPort))
    rFile.write("MariaDB DB Name: %s" % (rDatabase))
    rFile.write("MariaDB Username: %s\nMariaDB Password: %s" % (rUsername, rPassword))
    rFile.write("\nContinue Setup: http://%s/%s" % (getIP(), rCode))
    rFile.close()
    
    printc("Installation completed!", col.OKGREEN, 2)
    printc("Continue Setup: http://%s/%s" % (getIP(), rCode))
    print(" ")
    printc("Your mysql credentials have been saved to:")
    printc(rPath + "/credentials.txt")
    print(" ")
    printc("Please move this file somewhere safe!")
