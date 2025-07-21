"""
Main toolbar widget
"""

from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QLabel, 
                            QFrame, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction

class ToolbarWidget(QWidget):
    """Main application toolbar"""
    
    load_images_requested = pyqtSignal()
    export_requested = pyqtSignal()
    stitch_requested = pyqtSignal()
    reset_requested = pyqtSignal()
    delete_requested = pyqtSignal()
    selection_tool_toggled = pyqtSignal(bool)  # active state
    group_transform_requested = pyqtSignal(str, object)  # transform_type, value
    
    def __init__(self):
        super().__init__()
        self.selection_tool_active = False
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the toolbar UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Load button
        self.load_btn = QPushButton("📁 Load Images")
        self.load_btn.setToolTip("Load tissue fragment images (Ctrl+O)")
        self.load_btn.clicked.connect(self.load_images_requested)
        layout.addWidget(self.load_btn)
        
        # Selection tool button
        self.selection_btn = QPushButton("🔲 Select")
        self.selection_btn.setToolTip("Rectangle selection tool for multiple fragments")
        self.selection_btn.setCheckable(True)
        self.selection_btn.clicked.connect(self.toggle_selection_tool)
        layout.addWidget(self.selection_btn)
        
        # Separator
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.VLine)
        layout.addWidget(separator1)
        
        # Group transform buttons (initially hidden)
        self.group_rotate_cw_btn = QPushButton("↻ Group")
        self.group_rotate_cw_btn.setToolTip("Rotate selected group clockwise")
        self.group_rotate_cw_btn.clicked.connect(lambda: self.group_transform_requested.emit('rotate_cw', None))
        self.group_rotate_cw_btn.setVisible(False)
        layout.addWidget(self.group_rotate_cw_btn)
        
        self.group_rotate_ccw_btn = QPushButton("↺ Group")
        self.group_rotate_ccw_btn.setToolTip("Rotate selected group counter-clockwise")
        self.group_rotate_ccw_btn.clicked.connect(lambda: self.group_transform_requested.emit('rotate_ccw', None))
        self.group_rotate_ccw_btn.setVisible(False)
        layout.addWidget(self.group_rotate_ccw_btn)
        
        # Export button
        self.export_btn = QPushButton("💾 Export")
        self.export_btn.setToolTip("Export composite image and metadata")
        self.export_btn.clicked.connect(self.export_requested)
        self.export_btn.setEnabled(False)
        layout.addWidget(self.export_btn)
        
        # Separator
        separator2 = QFrame()  # Create a QFrame instead of QSeparator
        separator2.setFrameShape(QFrame.Shape.VLine)
        separator2.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator2)
        
        # Stitch button
        self.stitch_btn = QPushButton("🔗 Rigid Stitch")
        self.stitch_btn.setToolTip("Perform rigid stitching refinement (Ctrl+S)")
        self.stitch_btn.clicked.connect(self.stitch_requested)
        self.stitch_btn.setEnabled(False)
        layout.addWidget(self.stitch_btn)
        
        # Reset button
        self.reset_btn = QPushButton("🔄 Reset")
        self.reset_btn.setToolTip("Reset all transformations (Ctrl+R)")
        self.reset_btn.clicked.connect(self.reset_requested)
        self.reset_btn.setEnabled(False)
        layout.addWidget(self.reset_btn)
        
        # Delete button
        self.delete_btn = QPushButton("🗑️ Delete")
        self.delete_btn.setToolTip("Delete selected fragment (Del)")
        self.delete_btn.clicked.connect(self.delete_requested)
        self.delete_btn.setEnabled(False)
        layout.addWidget(self.delete_btn)
        
        # Spacer
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(spacer)
        
        # Status info
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #4a90e2; font-weight: bold;")
        layout.addWidget(self.status_label)
        
    def toggle_selection_tool(self):
        """Toggle selection tool state"""
        self.selection_tool_active = not self.selection_tool_active
        self.selection_btn.setChecked(self.selection_tool_active)
        
        # Show/hide group transform buttons
        self.group_rotate_cw_btn.setVisible(self.selection_tool_active)
        self.group_rotate_ccw_btn.setVisible(self.selection_tool_active)
        
        # Update button style
        if self.selection_tool_active:
            self.selection_btn.setStyleSheet("QPushButton { background-color: #4a90e2; }")
            self.status_label.setText("Selection tool active - drag to select multiple fragments")
        else:
            self.selection_btn.setStyleSheet("")
            self.status_label.setText("Ready")
            
        self.selection_tool_toggled.emit(self.selection_tool_active)
        
    def set_fragment_count(self, count: int):
        """Update the fragment count display"""
        if count == 0:
            if not self.selection_tool_active:
                self.status_label.setText("Ready")
            self.export_btn.setEnabled(False)
            self.stitch_btn.setEnabled(False)
            self.reset_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
        else:
            if not self.selection_tool_active:
                self.status_label.setText(f"{count} fragment{'s' if count != 1 else ''} loaded")
            self.export_btn.setEnabled(True)
            self.stitch_btn.setEnabled(count >= 2)
            self.reset_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
            
    def set_status(self, status: str):
        """Set the status message"""
        if not self.selection_tool_active:
            self.status_label.setText(status)