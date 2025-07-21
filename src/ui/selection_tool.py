"""
Selection tool for group operations
"""

from typing import List, Optional, Tuple, Set
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QPoint
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush

from ..core.fragment import Fragment

class SelectionTool:
    """Tool for selecting multiple fragments with rectangle selection"""
    
    def __init__(self):
        self.is_active = False
        self.is_selecting = False
        self.selection_start = QPoint()
        self.selection_end = QPoint()
        self.selected_fragment_ids: Set[str] = set()
        
    def start_selection(self, start_point: QPoint):
        """Start rectangle selection"""
        self.is_selecting = True
        self.selection_start = start_point
        self.selection_end = start_point
        
    def update_selection(self, end_point: QPoint):
        """Update selection rectangle"""
        if self.is_selecting:
            self.selection_end = end_point
            
    def finish_selection(self, fragments: List[Fragment]) -> Set[str]:
        """Finish selection and return selected fragment IDs"""
        if not self.is_selecting:
            return self.selected_fragment_ids
            
        self.is_selecting = False
        
        # Calculate selection rectangle
        selection_rect = QRect(self.selection_start, self.selection_end).normalized()
        
        # Find fragments within selection
        self.selected_fragment_ids.clear()
        for fragment in fragments:
            if not fragment.visible:
                continue
                
            bbox = fragment.get_bounding_box()
            fragment_rect = QRect(int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]))
            
            if selection_rect.intersects(fragment_rect):
                self.selected_fragment_ids.add(fragment.id)
                
        return self.selected_fragment_ids
        
    def cancel_selection(self):
        """Cancel current selection"""
        self.is_selecting = False
        
    def clear_selection(self):
        """Clear all selections"""
        self.selected_fragment_ids.clear()
        
    def get_selection_rect(self) -> QRect:
        """Get current selection rectangle"""
        if self.is_selecting:
            return QRect(self.selection_start, self.selection_end).normalized()
        return QRect()
        
    def draw_selection(self, painter: QPainter, zoom: float):
        """Draw selection rectangle"""
        if not self.is_selecting:
            return
            
        selection_rect = self.get_selection_rect()
        if selection_rect.isEmpty():
            return
            
        # Draw selection rectangle
        pen = QPen(QColor(74, 144, 226), 2.0 / zoom, Qt.PenStyle.DashLine)
        brush = QBrush(QColor(74, 144, 226, 30))
        
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRect(selection_rect)