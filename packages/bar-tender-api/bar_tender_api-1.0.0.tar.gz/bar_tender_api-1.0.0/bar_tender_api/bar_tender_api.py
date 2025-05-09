import logging
import os
import time
import clr
from typing import Dict, List, Optional


# noinspection PyUnresolvedReferences
class BarTenderApi:
    """BarTender 标签打印控制类。

    该类提供以下功能：
    - 初始化和管理 BarTender 引擎
    - 处理打印机连接
    - 打开和管理标签模板
    - 设置和获取标签变量
    - 执行打印任务
    """

    dll_path = f"{os.path.dirname(__file__)}/print_dll/Seagull.BarTender.Print.dll"

    def __init__(self):
        """初始化 BarTender 控制器."""
        clr.AddReference(self.dll_path)
        from Seagull.BarTender.Print import Engine, Printers

        self.logger = logging.getLogger("BarTenderApi")
        self.close_bar_tender()
        self._bar_engine = Engine(True)  # True 表示可见模式
        self._bar_engine_state = True
        self._btw_path = None
        self.printers = Printers()
        self.printer = self.printers.Default
        self.printer_name = self.printer.PrinterName
        self.bar_format = None

    def close_bar_tender(self):
        """强制关闭 BarTender 进程。"""
        cmd = "taskkill /IM bartend.exe /F"
        os.system(cmd)
        time.sleep(1)
        self.bar_engine_state = False

    def get_printer_list(self) -> List[str]:
        """获取可用的打印机列表。

        Returns:
            包含所有可用打印机名称的列表
        """
        printer_list = []
        for printer in self.printers:
            printer_list.append(printer.PrinterName)
        return printer_list

    @property
    def bar_engine(self):
        """返回当前驱动."""
        return self._bar_engine

    @bar_engine.setter
    def bar_engine(self, value):
        """设置 引擎.

        Args:
            value: Engine 实例.
        """
        self._bar_engine = value
        self.bar_engine_state = True

    @property
    def bar_engine_state(self):
        """返回当前驱动打开状态."""
        return self._bar_engine_state

    @bar_engine_state.setter
    def bar_engine_state(self, value: bool):
        """设置 引擎打开状态.

        Args:
            value: True -> 已打开, False -> 未打开.
        """
        self._bar_engine_state = value

    @property
    def btw_path(self):
        """返回要打印的 btw 文件路径."""
        return self._btw_path

    @btw_path.setter
    def btw_path(self, value: str):
        """设置 btw 文件路径.

        Args:
            value: btw 文件绝对路径.
        """
        self._btw_path = value

    def open_btw(self) -> bool:
        """创建打印任务并打开模板文件。

        Returns:
            bool: 模板是否成功打开
        """
        try:
            self.bar_format = self._bar_engine.Documents.Open(self.btw_path)
            if self.bar_format:
                self.bar_format.PrintSetup.PrinterName = self.printer_name
                return True
            return False
        except Exception as e:
            self.logger.warning("打开模板失败: %s", str(e))
            return False

    def close_btw(self):
        """关闭 btw 文件."""
        self.bar_format.Close()
        self.bar_format = False

    def print_job(self, job_name: str = "默认打印任务", timeout: int = 2000) -> bool:
        """执行打印任务。

        Args:
            job_name: 打印任务名称
            timeout: 超时时间(毫秒)

        Returns:
            bool: 打印是否成功
        """
        if not self.bar_format:
            self.logger.warning("错误: 未加载模板文件")
            return False

        try:
            result = self.bar_format.Print(job_name, timeout)
            return result == 0  # 0 表示成功
        except Exception as e:
            self.logger.warning("打印失败: %s", str(e))
            return False

    def get_data_dict(self, key: Optional[str] = None) -> Dict[str, str]:
        """获取模板中的所有变量或指定变量的值。

        Args:
            key: 可选，指定要获取的变量名

        Returns:
            如果指定了 key，返回该变量的值
            否则返回包含所有变量名和值的字典
        """
        data_dict = {}
        if self.bar_format:
            if key:
                return self.bar_format.SubStrings[key].Value
            for substring in self.bar_format.SubStrings:
                data_dict[substring.Name] = substring.Value
        return data_dict

    def set_data_dict(self, data_dict: Dict[str, str]) -> bool:
        """设置模板变量的值。

        Args:
            data_dict: 包含变量名和值的字典

        Returns:
            bool: 是否成功设置所有变量
        """
        if not self.bar_format or not data_dict:
            return False

        success = True
        for sub_string in self.bar_format.SubStrings:
            key = sub_string.Name.strip()
            if value := data_dict.get(key):
                self.bar_format.SubStrings.SetSubString(sub_string.Name, str(value))
        return success

    def __del__(self):
        """析构函数，确保资源被正确释放。"""
        try:
            if hasattr(self, "bar_format") and self.bar_format:
                self.bar_format.Close()
            if hasattr(self, "bar_engine") and self._bar_engine.IsAlive:
                self._bar_engine.Stop()
        except Exception as e:
            self.logger.info("资源释放时出错: %s", str(e))

    def execute_print(
            self, btw_path: str, update_data: Dict[str, str] = None,
            close_btw: bool = True, close_engine: bool = True
    ) -> bool:
        """执行打印.

        Args:
            btw_path: 要打印的模板文件路径.
            update_data: 要更新的数据, 默认 None.
            close_btw: 打印完是否关闭模板文件.
            close_engine: 打印完是否关闭 bar tender引擎.

        Returns:
            bool: True -> 打印成功, False -> 打印失败.
        """
        self.btw_path = btw_path
        if self.open_btw():
            if update_data:
                self.set_data_dict(update_data)
            print_state = self.print_job()
            if close_btw:
                self.close_btw()
            if close_engine:
                self.close_bar_tender()
            return print_state
        return False
