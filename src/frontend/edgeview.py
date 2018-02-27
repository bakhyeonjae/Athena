from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

import math

class EdgeView(object):

    def __init__(self, core):
        self.core = core
        self.margin = 5
        self.highlighted = False

    def updatePortPos(self, source, target):
        if source:
            self.setSrcCoord(source)
        if target:
            self.setDstCoord(target)

    def setSrcCoord(self, pos):
        self.srcPos = pos

    def setDstCoord(self, pos):
        self.dstPos = pos

    def getSrcCoord(self):
        return self.srcPos

    def getDstCoord(self):
        return self.dstPos

    def isOnEdge(self, pos):
        x0 = pos.x()
        y0 = pos.y()
        x1 = self.srcPos.x()
        y1 = self.srcPos.y()
        x2 = self.dstPos.x()
        y2 = self.dstPos.y()

        br = x1 if x1 > x2 else x2  # right boundary
        bl = x1 if x1 <= x2 else x2 # left boundary
        bt = y1 if y1 <= y2 else y2 # top boundary
        bb = y1 if y1 > y2 else y2 # bottom boundary

        if x0 < bl or x0 > br:
            return False
        if y0 < bt or y0 > bb:
            return False

        dist = math.fabs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1)
        dist /= math.sqrt((y2-y1)*(y2-y1) + (x2-x1)*(x2-x1))

        if dist > self.margin:
            return False

        return True

    def setHighlight(self, flag):
        self.highlighted = flag

    def isHighlighted(self):
        return self.highlighted

    def drawLine(self, painter):

        pen_restore = painter.pen()
        if self.highlighted:
            highlight_pen = QPen(QColor(0,0,0))
            highlight_pen.setWidth(2)        
            painter.setPen(highlight_pen)

        arrow_style = 'narrow-short'
        painter.drawPolygon(self.createArrowHead(self.getSrcCoord(),self.getDstCoord(),arrow_style))
        painter.drawLine(self.getSrcCoord(),self.getDstCoord())        

        if self.highlighted:
            painter.setPen(pen_restore)

    def createArrowHead(self,s,d,style):
        arrow_style = {'narrow-long':{'length':30, 'width':5},
                       'wide-long':{'length':30, 'width':20},
                       'narrow-short':{'length':15, 'width':5},
                       'wide-short':{'length':15, 'width':5}}
        polygon = QPolygonF()
        dx = d.x() - s.x()
        dy = d.y() - s.y()
        l = math.sqrt(dx*dx+dy*dy)
        rv = QPointF(s.x()-d.x(),s.y()-d.y())/l   # reverse vector
        nv = QPointF(s.y()-d.y(),d.x()-s.x())/l   # normal vector
        ep = QPointF(d.x(),d.y())                 # end point
        polygon.append(ep)
        polygon.append(ep+arrow_style[style]['length']*rv+arrow_style[style]['width']*nv)
        polygon.append(ep+arrow_style[style]['length']*rv-arrow_style[style]['width']*nv)
        return polygon
