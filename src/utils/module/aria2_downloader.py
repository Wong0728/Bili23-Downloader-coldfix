import os
import time
import json
import socket
import subprocess
import threading
from typing import Optional, Dict, Callable
from urllib.request import urlopen, Request
from urllib.error import URLError

from utils.config import Config
from utils.common.model.task_info import DownloadTaskInfo
from utils.common.model.callback import DownloaderCallback
from utils.common.formatter.formatter import FormatUtils
from utils.common.thread import Thread
from utils.common.request import RequestUtils

from utils.module.aria2.env import Aria2Env


class Aria2RPCClient:
    """ARIA2 RPC 客户端"""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 6800, secret: str = None):
        self.host = host
        self.port = port
        self.secret = secret
        self.rpc_url = f"http://{host}:{port}/jsonrpc"
    
    def call(self, method: str, params: list = None) -> dict:
        """调用 ARIA2 RPC 方法"""
        payload = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": method,
            "params": params or []
        }
        
        if self.secret:
            payload["params"].insert(0, f"token:{self.secret}")
        
        try:
            req = Request(
                self.rpc_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            
            with urlopen(req, timeout=5) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as e:
            return {"error": str(e)}
    
    def add_uri(self, uris: list, options: dict = None) -> str:
        """添加下载任务"""
        params = [uris]
        if options:
            params.append(options)
        
        result = self.call("aria2.addUri", params)
        return result.get("result") if "result" in result else None
    
    def tell_status(self, gid: str) -> dict:
        """获取任务状态"""
        result = self.call("aria2.tellStatus", [gid])
        return result.get("result", {})
    
    def remove(self, gid: str) -> bool:
        """移除任务"""
        result = self.call("aria2.remove", [gid])
        return "result" in result
    
    def pause(self, gid: str) -> bool:
        """暂停任务"""
        result = self.call("aria2.pause", [gid])
        return "result" in result
    
    def unpause(self, gid: str) -> bool:
        """恢复任务"""
        result = self.call("aria2.unpause", [gid])
        return "result" in result
    
    def get_global_stat(self) -> dict:
        """获取全局统计信息"""
        result = self.call("aria2.getGlobalStat")
        return result.get("result", {})


class Aria2Manager:
    """ARIA2 进程管理器（单例模式）"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.process: Optional[subprocess.Popen] = None
        self.is_running = False
        self.session_file = os.path.join(os.getcwd(), "data", "aria2.session")
        
        # RPC 客户端（根据配置初始化）
        self._init_rpc_client()
    
    def _init_rpc_client(self):
        """根据配置初始化 RPC 客户端"""
        if Config.Download.aria2_mode == 1:  # RPC 模式
            self.rpc_client = Aria2RPCClient(
                host=Config.Download.aria2_rpc_host,
                port=Config.Download.aria2_rpc_port,
                secret=Config.Download.aria2_rpc_secret
            )
        else:  # 本地模式
            self.rpc_client = Aria2RPCClient(port=6800)
    
    def get_aria2_path(self) -> str:
        """获取 ARIA2 可执行文件路径"""
        # 优先使用用户配置的路径
        if Config.Download.aria2_path and Aria2Env.check_file(Config.Download.aria2_path):
            return Config.Download.aria2_path
        
        # 自动检测
        detected = Aria2Env.detect_local_aria2()
        if detected:
            return detected
        
        return ""
    
    def is_port_available(self, port: int) -> bool:
        """检查端口是否可用"""
        return Aria2Env.is_port_available(port)
    
    def start(self) -> bool:
        """启动 ARIA2 服务"""
        # 重新初始化 RPC 客户端（配置可能已更改）
        self._init_rpc_client()
        
        if Config.Download.aria2_mode == 1:  # RPC 模式
            return self._start_rpc_mode()
        else:  # 本地模式
            return self._start_local_mode()
    
    def _start_rpc_mode(self) -> bool:
        """启动 RPC 模式（连接到外部 ARIA2）"""
        # 检查 RPC 服务是否可用
        if Aria2Env.check_rpc_available(
            Config.Download.aria2_rpc_host,
            Config.Download.aria2_rpc_port,
            Config.Download.aria2_rpc_secret
        ):
            self.is_running = True
            return True
        
        return False
    
    def _start_local_mode(self) -> bool:
        """启动本地模式（启动内置 ARIA2 进程）"""
        if self.is_running and self.process:
            # 检查进程是否仍在运行
            if self.process.poll() is None:
                return True
            else:
                self.is_running = False
        
        # 检查端口是否被占用
        if not self.is_port_available(self.rpc_client.port):
            # 端口被占用，可能是 ARIA2 已经在运行
            self.is_running = True
            return True
        
        aria2_path = self.get_aria2_path()
        if not aria2_path:
            print("未找到 ARIA2 可执行文件")
            return False
        
        # 确保 session 文件存在
        session_dir = os.path.dirname(self.session_file)
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)
        if not os.path.exists(self.session_file):
            open(self.session_file, "w").close()
        
        # 构建启动参数
        cmd = [
            aria2_path,
            "--enable-rpc=true",
            f"--rpc-listen-port={self.rpc_client.port}",
            "--rpc-allow-origin-all=true",
            "--rpc-listen-all=false",
            "--rpc-max-request-size=1024M",
            f"--split={Config.Download.aria2_thread_count}",
            f"--max-connection-per-server={Config.Download.aria2_thread_count}",
            "--min-split-size=1M",
            "--max-concurrent-downloads=5",
            "--max-tries=5",
            "--retry-wait=3",
            "--timeout=60",
            "--connect-timeout=30",
            "--disk-cache=32M",
            "--file-allocation=none",
            "--continue=true",
            f"--input-file={self.session_file}",
            f"--save-session={self.session_file}",
            "--save-session-interval=30",
            "--force-save=false",
            "--log-level=warn"
        ]
        
        # 代理设置
        if Config.Proxy.proxy_mode == 1:  # Custom
            cmd.extend([
                f"--all-proxy=http://{Config.Proxy.proxy_ip}:{Config.Proxy.proxy_port}"
            ])
        
        try:
            # 启动 ARIA2 进程
            if os.name == "nt":  # Windows
                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            
            # 等待 ARIA2 启动
            for _ in range(10):
                time.sleep(0.5)
                if not self.is_port_available(self.rpc_client.port):
                    self.is_running = True
                    return True
            
            return False
            
        except Exception as e:
            print(f"启动 ARIA2 失败: {e}")
            return False
    
    def stop(self):
        """停止 ARIA2 进程（仅本地模式）"""
        if Config.Download.aria2_mode == 0 and self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                self.process.kill()
            finally:
                self.process = None
                self.is_running = False
    
    def shutdown(self):
        """通过 RPC 关闭 ARIA2"""
        self.rpc_client.call("aria2.shutdown")
        self.is_running = False
    
    def get_download_speed(self) -> int:
        """获取当前下载速度（字节/秒）"""
        try:
            stat = self.rpc_client.get_global_stat()
            download_speed = stat.get("downloadSpeed", "0")
            return int(download_speed)
        except:
            return 0


class Aria2Downloader:
    """ARIA2 下载器"""
    
    def __init__(self, task_info: DownloadTaskInfo, callback: DownloaderCallback):
        self.task_info = task_info
        self.callback = callback
        self.manager = Aria2Manager()
        self.rpc = self.manager.rpc_client
        
        self.stop_event = threading.Event()
        self.gid: Optional[str] = None
        self.lock = threading.Lock()
        
        self.download_path = self._get_download_path()
        self.downloader_info_list = []
        self.current_file_index = 0
        self.total_downloaded = 0
        self.current_file_downloaded = 0
        
        # 速度监控
        self.current_speed = 0
    
    def _get_download_path(self) -> str:
        """获取下载路径"""
        from utils.common.formatter.file_name_v2 import FileNameFormatter
        return FileNameFormatter.get_download_path(self.task_info)
    
    def set_downloader_info(self, downloader_info: list):
        """设置下载信息"""
        self.downloader_info_list = downloader_info
        
        # 计算总文件大小
        total_size = 0
        for info in downloader_info:
            url_list = info.get("url_list", [])
            if url_list:
                from utils.module.web.cdn import CDN
                size_info = CDN.get_file_size(url_list)
                if size_info:
                    total_size += size_info[1]
        
        self.task_info.total_file_size = total_size
    
    def start_download(self):
        """开始下载"""
        if not self.manager.start():
            raise Exception("无法启动 ARIA2")
        
        self.callback.onStart()
        
        # 开始第一个文件下载
        self._download_next_file()
    
    def _download_next_file(self):
        """下载下一个文件"""
        if self.stop_event.is_set():
            return
        
        if self.current_file_index >= len(self.downloader_info_list):
            # 所有文件下载完成
            self.callback.onComplete()
            return
        
        info = self.downloader_info_list[self.current_file_index]
        url_list = info.get("url_list", [])
        file_name = info.get("file_name")
        download_type = info.get("type")
        
        if not url_list:
            self.current_file_index += 1
            self._download_next_file()
            return
        
        # 获取实际下载 URL
        from utils.module.web.cdn import CDN
        url_info = CDN.get_file_size(url_list)
        if not url_info:
            self.callback.onError()
            return
        
        actual_url = url_info[0]
        file_size = url_info[1]
        
        self.current_file_downloaded = 0
        
        # 构建 ARIA2 选项
        headers = RequestUtils.get_headers(
            referer_url=self.task_info.referer_url,
            sessdata=Config.User.SESSDATA
        )
        
        options = {
            "dir": self.download_path,
            "out": file_name,
            "referer": self.task_info.referer_url,
            "header": [f"{k}: {v}" for k, v in headers.items() if k != "Cookie"],
            "continue": "true"
        }
        
        # 添加 Cookie
        if "Cookie" in headers:
            options["header"].append(f"Cookie: {headers['Cookie']}")
        
        # 速度限制
        if Config.Download.enable_speed_limit:
            max_speed = int(Config.Download.speed_mbps * 1024 * 1024)
            options["max-download-limit"] = str(max_speed)
        
        # 添加下载任务
        self.gid = self.rpc.add_uri([actual_url], options)
        
        if not self.gid:
            self.callback.onError()
            return
        
        # 启动进度监听
        Thread(target=self._monitor_progress, args=(download_type, file_name, file_size)).start()
    
    def _monitor_progress(self, download_type: str, file_name: str, file_size: int):
        """监控下载进度"""
        last_downloaded = 0
        last_time = time.time()
        
        while not self.stop_event.is_set():
            try:
                status = self.rpc.tell_status(self.gid)
                
                if not status:
                    time.sleep(0.5)
                    continue
                
                state = status.get("status", "")
                
                if state == "error":
                    with self.lock:
                        if not self.stop_event.is_set():
                            self.callback.onError()
                    return
                
                if state == "complete":
                    # 当前文件完成，更新总进度
                    self.total_downloaded += file_size
                    
                    # 更新任务信息到 100%（确保 UI 显示最终进度）
                    if self.task_info.total_file_size > 0:
                        total_progress = (self.total_downloaded / self.task_info.total_file_size) * 100
                    else:
                        total_progress = 100
                    
                    self.task_info.progress = int(total_progress)
                    self.task_info.current_downloaded_size = file_size
                    self.task_info.total_downloaded_size = self.total_downloaded
                    self.task_info.update()
                    
                    # 回调更新进度
                    self.callback.onDownloading(FormatUtils.format_speed(0))
                    
                    # 从下载项中移除
                    if download_type in self.task_info.download_items:
                        self.task_info.download_items.remove(download_type)
                    
                    self.current_file_index += 1
                    self._download_next_file()
                    return
                
                # 计算进度和速度
                completed = int(status.get("completedLength", 0))
                total = int(status.get("totalLength", file_size))
                
                # 计算下载速度
                download_speed = int(status.get("downloadSpeed", 0))
                self.current_speed = download_speed
                
                # 计算总体进度
                current_total_downloaded = self.total_downloaded + completed
                if self.task_info.total_file_size > 0:
                    total_progress = (current_total_downloaded / self.task_info.total_file_size) * 100
                else:
                    total_progress = 0
                
                # 计算速度（用于回调显示）
                current_time = time.time()
                time_diff = current_time - last_time
                
                if time_diff >= 1.0:
                    speed = (completed - last_downloaded) / time_diff
                    last_downloaded = completed
                    last_time = current_time
                    
                    # 更新任务信息
                    self.task_info.progress = int(total_progress)
                    self.task_info.current_downloaded_size = completed
                    self.task_info.total_downloaded_size = current_total_downloaded
                    self.task_info.update()
                    
                    # 回调更新速度
                    self.callback.onDownloading(FormatUtils.format_speed(speed))
                
                time.sleep(0.5)
                
            except Exception as e:
                print(f"监控进度出错: {e}")
                time.sleep(1)
    
    def stop_download(self):
        """停止下载"""
        self.stop_event.set()
        
        if self.gid:
            try:
                self.rpc.pause(self.gid)
            except:
                pass
    
    def resume_download(self):
        """恢复下载"""
        self.stop_event.clear()
        
        if self.gid:
            try:
                self.rpc.unpause(self.gid)
            except:
                pass
    
    def retry_download(self):
        """重试下载"""
        if self.gid:
            try:
                self.rpc.remove(self.gid)
            except:
                pass
        
        self.stop_event.clear()
        self._download_next_file()
    
    def get_speed(self) -> str:
        """获取当前下载速度（格式化字符串）"""
        return FormatUtils.format_speed(self.current_speed)
