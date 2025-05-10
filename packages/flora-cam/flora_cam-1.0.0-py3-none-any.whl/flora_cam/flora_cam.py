from enum import Enum
from typing import Any, Optional

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber

class FloraCam(ConstrainedControl):
    def __init__(
        self,
        opacity: OptionalNumber = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Optional[bool] = None,
    ):
        ConstrainedControl.__init__(
            self,
            tooltip=tooltip,
            opacity=opacity,
            visible=visible,
            data=data,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            width=width,
            height=height
        )

    def _get_control_name(self):
        return "FloraCam"
    
    def camera_mode(self, comment: str = "", wait_timeout: Optional[float] = 25):
        out = self.invoke_method(
            "camera_mode",
            {"comment": comment if isinstance(comment, str) else comment},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
    
    def switch_camera(self, comment: str = "", wait_timeout: Optional[float] = 25):
        out = self.invoke_method(
            "switch_camera",
            {"comment": comment if isinstance(comment, str) else comment},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
    
    def take_picture(self, comment: str = "", wait_timeout: Optional[float] = 25):
        out = self.invoke_method(
            "take_picture",
            {"comment": comment if isinstance(comment, str) else comment},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return str(out)