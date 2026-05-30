from datetime import datetime

from PyQt6 import QtCore, QtGui, QtWidgets


PAGE_BG = "#f8fbff"
CARD_BORDER = "#EAECF0"
TEXT = "#0f172a"
MUTED = "#667085"
GREEN = "#16B364"


def parse_datetime(value):
    if isinstance(value, datetime):
        return value
    text = str(value or "").strip()
    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
    ):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def age_from_dob(value):
    dob = parse_datetime(value)
    if not dob:
        return ""
    today = datetime.now().date()
    years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return f"{max(0, years)} tuổi"


def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        child = item.widget()
        if child:
            child.deleteLater()
        child_layout = item.layout()
        if child_layout:
            clear_layout(child_layout)


def page_title(title, breadcrumb):
    wrapper = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(wrapper)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(3)
    title_label = QtWidgets.QLabel(title)
    title_label.setStyleSheet(f"font-size: 23px; font-weight: 800; color: {TEXT}; background: transparent;")
    crumb_label = QtWidgets.QLabel(breadcrumb)
    crumb_label.setStyleSheet(f"font-size: 13px; color: {MUTED}; font-weight: 500; background: transparent;")
    layout.addWidget(title_label)
    layout.addWidget(crumb_label)
    return wrapper


def card(radius=16):
    frame = QtWidgets.QFrame()
    frame.setObjectName("doctorCard")
    frame.setStyleSheet(
        f"QFrame#doctorCard {{ background: white; border: 1px solid {CARD_BORDER}; border-radius: {radius}px; }}"
    )
    return frame


def badge(text, color="#12B76A", bg="#ECFDF3", min_width=0):
    label = QtWidgets.QLabel(str(text or ""))
    label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    if min_width:
        label.setMinimumWidth(min_width)
    label.setStyleSheet(
        f"background: {bg}; color: {color}; border: none; border-radius: 10px; "
        "padding: 5px 10px; font-size: 12px; font-weight: 800;"
    )
    return label


def initials(name):
    parts = [part for part in str(name or "").strip().split() if part]
    if not parts:
        return "BN"
    return "".join(part[0].upper() for part in parts[-2:])[:2]


def avatar(name, size=42, bg="#EAF7F0", color=GREEN):
    label = QtWidgets.QLabel(initials(name))
    label.setFixedSize(size, size)
    label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet(
        f"background: {bg}; color: {color}; border: none; border-radius: {size // 2}px; "
        "font-size: 14px; font-weight: 800;"
    )
    return label


def input_style():
    return (
        "background: white; color: #344054; border: 1px solid #D0D5DD; border-radius: 10px; "
        "padding: 7px 11px; font-size: 13px; font-weight: 500;"
    )


def table_style():
    return (
        "QTableWidget { background: white; color: #344054; border: none; gridline-color: transparent; font-size: 13px; }"
        "QHeaderView::section { background: white; color: #101828; border: none; border-bottom: 1px solid #EAECF0; "
        "padding: 7px 6px; font-weight: 800; font-size: 13px; }"
        "QTableWidget::item { border-bottom: 1px solid #F2F4F7; padding: 5px; }"
        "QTableWidget::item:selected { background: #ECFDF3; color: #101828; }"
    )


def button(text, kind="primary"):
    btn = QtWidgets.QPushButton(text)
    btn.setMinimumHeight(34)
    btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    if kind == "primary":
        css = "background: #16B364; color: white; border: none;"
    elif kind == "danger":
        css = "background: white; color: #F04438; border: 1px solid #FEE4E2;"
    else:
        css = "background: white; color: #344054; border: 1px solid #D0D5DD;"
    btn.setStyleSheet(f"QPushButton {{ {css} border-radius: 9px; padding: 7px 12px; font-weight: 800; }}")
    return btn


def icon_button(text):
    btn = QtWidgets.QPushButton(text)
    btn.setFixedSize(30, 30)
    btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    btn.setStyleSheet(
        "QPushButton { background: white; color: #475467; border: 1px solid #EAECF0; "
        "border-radius: 9px; font-size: 13px; font-weight: 800; }"
        "QPushButton:hover { background: #F9FAFB; }"
    )
    return btn
