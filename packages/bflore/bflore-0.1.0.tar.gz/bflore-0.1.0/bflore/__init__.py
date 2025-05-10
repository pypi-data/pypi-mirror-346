"""
Bflore - مكتبة لتوسيع إمكانيات Flask مع دعم للروابط المحلية المخصصة
"""

__version__ = '0.1.0'

from .core import BfloreApp, run_with_custom_host
from .cli import main

__all__ = ['BfloreApp', 'run_with_custom_host']