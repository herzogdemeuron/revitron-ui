import sys
import os.path as op

dn = op.dirname
sys.path.append(op.join(dn(dn(__file__)), 'hdm-revitron.lib'))

from revitronui.history.events import HistoryEventHandler

HistoryEventHandler()