import os
import socket
import subprocess
import json

from utils.config import Config
from utils.common.enums import Platform


class Aria2Env:
    """ARIA2 环境检测与管理类"""
    
    RPC_DEFAULT_PORT = 6800
    RPC_DEFAULT_SECRET = ""
    
    @staticmethod
    def check_file(path: str) -> bool:
        """检查文件是否存在且可执行"""
        return os.path.isfile(path) and os.access(path, os.X_OK if os.name != "nt" else os.F_OK)
    
    @classmethod
    def get_executable_name(cls) -> str:
        """获取 ARIA2 可执行文件名"""
        match Platform(Config.Sys.platform):
            case Platform.Windows:
                return "aria2c.exe"
            case Platform.Linux | Platform.macOS:
                return "aria2c"
    
    @classmethod
    def get_env_path(cls) -> str:
        """从环境变量 PATH 中查找 ARIA2"""
        path_env = os.environ.get("PATH", "")
        executable = cls.get_executable_name()
        
        for directory in path_env.split(os.pathsep):
            possible_path = os.path.join(directory, executable)
            if cls.check_file(possible_path):
                return possible_path
        return ""
    
    @classmethod
    def get_cwd_path(cls) -> str:
        """从程序运行目录查找 ARIA2"""
        executable = cls.get_executable_name()
        possible_path = os.path.join(os.getcwd(), executable)
        if cls.check_file(possible_path):
            return possible_path
        return ""
    
    @classmethod
    def get_aria2_paths(cls) -> dict:
        """获取所有可能的 ARIA2 路径"""
        return {
            "env_path": cls.get_env_path(),
            "cwd_path": cls.get_cwd_path(),
        }
    
    @classmethod
    def detect_local_aria2(cls) -> str:
        """自动检测本地 ARIA2 路径"""
        paths = cls.get_aria2_paths()
        
        # 优先使用运行目录的 aria2c
        if paths["cwd_path"]:
            return paths["cwd_path"]
        
        # 其次使用环境变量中的 aria2c
        if paths["env_path"]:
            return paths["env_path"]
        
        return ""
    
    @classmethod
    def check_rpc_available(cls, host: str = "127.0.0.1", port: int = None, secret: str = None) -> bool:
        """检查 RPC 服务是否可用"""
        if port is None:
            port = Config.Download.aria2_rpc_port or cls.RPC_DEFAULT_PORT
        
        try:
            # 尝试连接 RPC 端口
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result != 0:
                return False
            
            # 尝试调用 RPC 方法验证
            from urllib.request import urlopen, Request
            
            rpc_url = f"http://{host}:{port}/jsonrpc"
            payload = {
                "jsonrpc": "2.0",
                "id": "1",
                "method": "aria2.getVersion",
                "params": []
            }
            
            if secret:
                payload["params"].insert(0, f"token:{secret}")
            
            req = Request(
                rpc_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            
            with urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode("utf-8"))
                return "result" in result
                
        except Exception:
            return False
        
        return False
    
    @classmethod
    def get_rpc_version(cls, host: str = "127.0.0.1", port: int = None, secret: str = None) -> str:
        """获取 RPC 服务端版本信息"""
        if port is None:
            port = Config.Download.aria2_rpc_port or cls.RPC_DEFAULT_PORT
        
        try:
            from urllib.request import urlopen, Request
            
            rpc_url = f"http://{host}:{port}/jsonrpc"
            payload = {
                "jsonrpc": "2.0",
                "id": "1",
                "method": "aria2.getVersion",
                "params": []
            }
            
            if secret:
                payload["params"].insert(0, f"token:{secret}")
            
            req = Request(
                rpc_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            
            with urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode("utf-8"))
                if "result" in result:
                    return result["result"].get("version", "")
        except Exception:
            pass
        
        return ""
    
    @classmethod
    def is_port_available(cls, port: int) -> bool:
        """检查端口是否可用（未被占用）"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(("127.0.0.1", port))
            sock.close()
            return result != 0
        except:
            return False
    
    @classmethod
    def get_local_aria2_version(cls, aria2_path: str) -> str:
        """获取本地 ARIA2 版本"""
        if not cls.check_file(aria2_path):
            return ""
        
        try:
            result = subprocess.run(
                [aria2_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                # 解析版本信息，第一行通常是 "aria2 version x.x.x"
                first_line = result.stdout.strip().split("\n")[0]
                if "version" in first_line:
                    return first_line.split("version")[1].strip()
        except Exception:
            pass
        
        return ""
    
    @classmethod
    def auto_detect_and_configure(cls):
        """自动检测并配置 ARIA2"""
        # 如果用户已经配置了路径，检查是否仍然有效
        current_path = Config.Download.aria2_path
        if current_path and cls.check_file(current_path):
            return
        
        # 自动检测本地 ARIA2
        detected_path = cls.detect_local_aria2()
        if detected_path:
            Config.Download.aria2_path = detected_path
            # 检测到本地 ARIA2，默认使用本地模式
            Config.Download.aria2_mode = 0  # 0=本地模式, 1=RPC模式
