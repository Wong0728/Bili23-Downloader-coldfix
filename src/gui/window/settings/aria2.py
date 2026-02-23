import wx
import os
import gettext

from utils.config import Config
from utils.common.enums import Platform
from utils.common.style.icon_v4 import Icon, IconID
from utils.module.aria2.env import Aria2Env

from gui.window.settings.page import Page
from gui.dialog.setting.aria2 import DetectDialog

from gui.component.misc.tooltip import ToolTip
from gui.component.button.bitmap_button import BitmapButton
from gui.component.slider.slider_box import SliderBox

_ = gettext.gettext


class Aria2Page(Page):
    """ARIA2 设置页面"""
    
    def __init__(self, parent: wx.Window):
        Page.__init__(self, parent, "ARIA2", 3)
        
        self.init_UI()
        self.Bind_EVT()
        self.load_data()
    
    def init_UI(self):
        # ARIA2 模式选择
        mode_box = wx.StaticBox(self.panel, -1, _("ARIA2 模式"))
        
        self.local_mode_radio = wx.RadioButton(mode_box, -1, _("本地模式（启动内置 ARIA2）"))
        self.rpc_mode_radio = wx.RadioButton(mode_box, -1, _("RPC 模式（连接外部 ARIA2）"))
        
        mode_tip = ToolTip(mode_box)
        mode_tip.set_tooltip(_("本地模式：程序自动启动内置的 ARIA2 进程\\nRPC 模式：连接到已运行的 ARIA2 服务（如 AriaNg、WebUI 等）"))
        
        mode_hbox = wx.BoxSizer(wx.HORIZONTAL)
        mode_hbox.Add(self.local_mode_radio, 0, wx.ALL | wx.ALIGN_CENTER, self.FromDIP(6))
        mode_hbox.Add(self.rpc_mode_radio, 0, wx.ALL | wx.ALIGN_CENTER, self.FromDIP(6))
        mode_hbox.Add(mode_tip, 0, wx.ALL | wx.ALIGN_CENTER, self.FromDIP(6))
        
        mode_sbox = wx.StaticBoxSizer(mode_box, wx.VERTICAL)
        mode_sbox.Add(mode_hbox, 0, wx.EXPAND)
        
        # 本地模式设置
        self.local_settings_box = wx.StaticBox(self.panel, -1, _("本地 ARIA2 设置"))
        
        aria2_path_label = wx.StaticText(self.local_settings_box, -1, _("ARIA2 路径"))
        self.path_box = wx.TextCtrl(self.local_settings_box, -1)
        self.browse_btn = BitmapButton(self.local_settings_box, Icon.get_icon_bitmap(IconID.Folder), tooltip=_("浏览"))
        
        path_hbox = wx.BoxSizer(wx.HORIZONTAL)
        path_hbox.Add(self.path_box, 1, wx.ALL & (~wx.TOP) | wx.ALIGN_CENTER, self.FromDIP(6))
        path_hbox.Add(self.browse_btn, 0, wx.ALL & (~wx.TOP) & (~wx.LEFT) | wx.ALIGN_CENTER, self.FromDIP(6))
        
        self.detect_btn = wx.Button(self.local_settings_box, -1, _("自动检测"), size=self.get_scaled_size((90, 28)))
        self.test_local_btn = wx.Button(self.local_settings_box, -1, _("测试"), size=self.get_scaled_size((90, 28)))
        
        local_btn_hbox = wx.BoxSizer(wx.HORIZONTAL)
        local_btn_hbox.Add(self.detect_btn, 0, wx.ALL & (~wx.TOP), self.FromDIP(6))
        local_btn_hbox.Add(self.test_local_btn, 0, wx.ALL & (~wx.TOP) & (~wx.LEFT), self.FromDIP(6))
        
        local_sbox = wx.StaticBoxSizer(self.local_settings_box, wx.VERTICAL)
        local_sbox.Add(aria2_path_label, 0, wx.ALL, self.FromDIP(6))
        local_sbox.Add(path_hbox, 0, wx.EXPAND)
        local_sbox.Add(local_btn_hbox, 0, wx.EXPAND)
        
        # RPC 模式设置
        self.rpc_settings_box = wx.StaticBox(self.panel, -1, _("RPC 连接设置"))
        
        rpc_host_label = wx.StaticText(self.rpc_settings_box, -1, _("主机地址"))
        self.rpc_host_box = wx.TextCtrl(self.rpc_settings_box, -1)
        
        rpc_port_label = wx.StaticText(self.rpc_settings_box, -1, _("端口"))
        self.rpc_port_box = wx.TextCtrl(self.rpc_settings_box, -1, size=self.FromDIP((80, -1)))
        
        rpc_secret_label = wx.StaticText(self.rpc_settings_box, -1, _("密钥（可选）"))
        self.rpc_secret_box = wx.TextCtrl(self.rpc_settings_box, -1, style=wx.TE_PASSWORD)
        
        self.test_rpc_btn = wx.Button(self.rpc_settings_box, -1, _("测试连接"), size=self.get_scaled_size((90, 28)))
        
        rpc_host_hbox = wx.BoxSizer(wx.HORIZONTAL)
        rpc_host_hbox.Add(rpc_host_label, 0, wx.ALL | wx.ALIGN_CENTER, self.FromDIP(6))
        rpc_host_hbox.Add(self.rpc_host_box, 1, wx.ALL & (~wx.LEFT) | wx.ALIGN_CENTER, self.FromDIP(6))
        
        rpc_port_hbox = wx.BoxSizer(wx.HORIZONTAL)
        rpc_port_hbox.Add(rpc_port_label, 0, wx.ALL | wx.ALIGN_CENTER, self.FromDIP(6))
        rpc_port_hbox.Add(self.rpc_port_box, 0, wx.ALL & (~wx.LEFT) | wx.ALIGN_CENTER, self.FromDIP(6))
        
        rpc_secret_hbox = wx.BoxSizer(wx.HORIZONTAL)
        rpc_secret_hbox.Add(rpc_secret_label, 0, wx.ALL | wx.ALIGN_CENTER, self.FromDIP(6))
        rpc_secret_hbox.Add(self.rpc_secret_box, 1, wx.ALL & (~wx.LEFT) | wx.ALIGN_CENTER, self.FromDIP(6))
        
        rpc_sbox = wx.StaticBoxSizer(self.rpc_settings_box, wx.VERTICAL)
        rpc_sbox.Add(rpc_host_hbox, 0, wx.EXPAND)
        rpc_sbox.Add(rpc_port_hbox, 0, wx.EXPAND)
        rpc_sbox.Add(rpc_secret_hbox, 0, wx.EXPAND)
        rpc_sbox.Add(self.test_rpc_btn, 0, wx.ALL & (~wx.TOP), self.FromDIP(6))
        
        # 下载选项设置
        download_option_box = wx.StaticBox(self.panel, -1, _("下载选项"))
        
        self.enable_aria2_chk = wx.CheckBox(download_option_box, -1, _("启用 ARIA2 多线程下载"))
        aria2_tip = ToolTip(download_option_box)
        aria2_tip.set_tooltip(_("使用 ARIA2 进行多线程下载，可以显著提升下载速度"))
        
        enable_hbox = wx.BoxSizer(wx.HORIZONTAL)
        enable_hbox.Add(self.enable_aria2_chk, 0, wx.ALL & (~wx.RIGHT) | wx.ALIGN_CENTER, self.FromDIP(6))
        enable_hbox.Add(aria2_tip, 0, wx.ALL | wx.ALIGN_CENTER, self.FromDIP(6))
        
        self.thread_count_lab = wx.StaticText(download_option_box, -1, _("线程数"))
        self.thread_count_slider = SliderBox(download_option_box, "", 16, 32)
        
        thread_hbox = wx.BoxSizer(wx.HORIZONTAL)
        thread_hbox.AddSpacer(self.FromDIP(20))
        thread_hbox.Add(self.thread_count_lab, 0, wx.ALL | wx.ALIGN_CENTER, self.FromDIP(6))
        thread_hbox.Add(self.thread_count_slider, 1, wx.ALL & (~wx.LEFT) | wx.EXPAND, self.FromDIP(6))
        
        download_option_sbox = wx.StaticBoxSizer(download_option_box, wx.VERTICAL)
        download_option_sbox.Add(enable_hbox, 0, wx.EXPAND)
        download_option_sbox.Add(thread_hbox, 0, wx.EXPAND)
        
        # 主布局
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(mode_sbox, 0, wx.ALL | wx.EXPAND, self.FromDIP(6))
        vbox.Add(local_sbox, 0, wx.ALL & (~wx.TOP) | wx.EXPAND, self.FromDIP(6))
        vbox.Add(rpc_sbox, 0, wx.ALL & (~wx.TOP) | wx.EXPAND, self.FromDIP(6))
        vbox.Add(download_option_sbox, 0, wx.ALL & (~wx.TOP) | wx.EXPAND, self.FromDIP(6))
        
        self.panel.SetSizer(vbox)
        super().init_UI()
    
    def Bind_EVT(self):
        self.local_mode_radio.Bind(wx.EVT_RADIOBUTTON, self.onModeChange)
        self.rpc_mode_radio.Bind(wx.EVT_RADIOBUTTON, self.onModeChange)
        
        self.browse_btn.Bind(wx.EVT_BUTTON, self.onBrowsePathEVT)
        self.detect_btn.Bind(wx.EVT_BUTTON, self.onDetectEVT)
        self.test_local_btn.Bind(wx.EVT_BUTTON, self.onTestLocalEVT)
        self.test_rpc_btn.Bind(wx.EVT_BUTTON, self.onTestRPCEVT)
        
        self.enable_aria2_chk.Bind(wx.EVT_CHECKBOX, self.onEnableChange)
    
    def load_data(self):
        # 加载模式设置
        if Config.Download.aria2_mode == 0:
            self.local_mode_radio.SetValue(True)
        else:
            self.rpc_mode_radio.SetValue(True)
        
        # 加载本地设置
        self.path_box.SetValue(Config.Download.aria2_path)
        
        # 加载 RPC 设置
        self.rpc_host_box.SetValue(Config.Download.aria2_rpc_host)
        self.rpc_port_box.SetValue(str(Config.Download.aria2_rpc_port))
        self.rpc_secret_box.SetValue(Config.Download.aria2_rpc_secret)
        
        # 加载下载选项
        self.enable_aria2_chk.SetValue(Config.Download.enable_aria2)
        self.thread_count_slider.SetValue(Config.Download.aria2_thread_count)
        
        self.update_ui_state()
    
    def save_data(self):
        Config.Download.aria2_mode = 0 if self.local_mode_radio.GetValue() else 1
        Config.Download.aria2_path = self.path_box.GetValue()
        Config.Download.aria2_rpc_host = self.rpc_host_box.GetValue()
        
        try:
            Config.Download.aria2_rpc_port = int(self.rpc_port_box.GetValue())
        except ValueError:
            Config.Download.aria2_rpc_port = 6800
        
        Config.Download.aria2_rpc_secret = self.rpc_secret_box.GetValue()
        Config.Download.enable_aria2 = self.enable_aria2_chk.GetValue()
        Config.Download.aria2_thread_count = self.thread_count_slider.GetValue()
    
    def onValidate(self):
        if self.local_mode_radio.GetValue():
            # 本地模式验证
            if not self.path_box.GetValue():
                return self.warn(_("ARIA2 路径不能为空"))
            
            if not Aria2Env.check_file(self.path_box.GetValue()):
                return self.warn(_("ARIA2 路径无效，文件不存在或无法访问"))
        else:
            # RPC 模式验证
            if not self.rpc_host_box.GetValue():
                return self.warn(_("RPC 主机地址不能为空"))
            
            try:
                port = int(self.rpc_port_box.GetValue())
                if not (1 <= port <= 65535):
                    raise ValueError()
            except ValueError:
                return self.warn(_("RPC 端口无效，请输入 1-65535 之间的数字"))
        
        self.save_data()
    
    def update_ui_state(self):
        """根据当前模式更新 UI 状态"""
        is_local_mode = self.local_mode_radio.GetValue()
        
        # 本地模式控件
        self.local_settings_box.Enable(is_local_mode)
        self.path_box.Enable(is_local_mode)
        self.browse_btn.Enable(is_local_mode)
        self.detect_btn.Enable(is_local_mode)
        self.test_local_btn.Enable(is_local_mode)
        
        # RPC 模式控件
        self.rpc_settings_box.Enable(not is_local_mode)
        self.rpc_host_box.Enable(not is_local_mode)
        self.rpc_port_box.Enable(not is_local_mode)
        self.rpc_secret_box.Enable(not is_local_mode)
        self.test_rpc_btn.Enable(not is_local_mode)
        
        # 下载选项
        is_enabled = self.enable_aria2_chk.GetValue()
        self.thread_count_lab.Enable(is_enabled)
        self.thread_count_slider.Enable(is_enabled)
    
    def onModeChange(self, event):
        self.update_ui_state()
    
    def onEnableChange(self, event):
        self.update_ui_state()
    
    def onBrowsePathEVT(self, event):
        default_dir = os.path.dirname(self.path_box.GetValue())
        
        match Platform(Config.Sys.platform):
            case Platform.Windows:
                defaultFile = "aria2c.exe"
                wildcard = "ARIA2|aria2c.exe"
            case Platform.Linux | Platform.macOS:
                defaultFile = "aria2c"
                wildcard = "ARIA2|*"
        
        dlg = wx.FileDialog(
            self, 
            _("选择 ARIA2 路径"), 
            defaultDir=default_dir, 
            defaultFile=defaultFile, 
            style=wx.FD_OPEN, 
            wildcard=wildcard
        )
        
        if dlg.ShowModal() == wx.ID_OK:
            self.path_box.SetValue(dlg.GetPath())
        
        dlg.Destroy()
    
    def onDetectEVT(self, event):
        detect_window = DetectDialog(self)
        
        if detect_window.ShowModal() == wx.ID_OK:
            self.path_box.SetValue(detect_window.getPath())
    
    def onTestLocalEVT(self, event):
        """测试本地 ARIA2"""
        path = self.path_box.GetValue()
        
        if not path:
            wx.MessageDialog(self, _("请先设置 ARIA2 路径"), _("提示"), wx.ICON_INFORMATION).ShowModal()
            return
        
        if not Aria2Env.check_file(path):
            wx.MessageDialog(self, _("ARIA2 文件不存在或无法访问"), _("错误"), wx.ICON_ERROR).ShowModal()
            return
        
        version = Aria2Env.get_local_aria2_version(path)
        
        if version:
            wx.MessageDialog(
                self, 
                _(f"ARIA2 可用\\n\\n版本: {version}"), 
                _("测试成功"), 
                wx.ICON_INFORMATION
            ).ShowModal()
        else:
            wx.MessageDialog(self, _("无法获取 ARIA2 版本信息"), _("错误"), wx.ICON_ERROR).ShowModal()
    
    def onTestRPCEVT(self, event):
        """测试 RPC 连接"""
        host = self.rpc_host_box.GetValue() or "127.0.0.1"
        
        try:
            port = int(self.rpc_port_box.GetValue())
        except ValueError:
            port = 6800
        
        secret = self.rpc_secret_box.GetValue()
        
        if Aria2Env.check_rpc_available(host, port, secret):
            version = Aria2Env.get_rpc_version(host, port, secret)
            wx.MessageDialog(
                self, 
                _(f"RPC 连接成功\\n\\nARIA2 版本: {version}"), 
                _("测试成功"), 
                wx.ICON_INFORMATION
            ).ShowModal()
        else:
            wx.MessageDialog(
                self, 
                _("无法连接到 ARIA2 RPC 服务\\n\\n请检查：\\n1. ARIA2 是否已启动并启用了 RPC\\n2. 主机地址和端口是否正确\\n3. 密钥是否正确（如果设置了密钥）"), 
                _("连接失败"), 
                wx.ICON_ERROR
            ).ShowModal()
