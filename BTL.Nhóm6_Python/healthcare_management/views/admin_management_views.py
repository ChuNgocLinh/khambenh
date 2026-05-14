import csv
import hashlib
import os
import shutil
from datetime import date, datetime, timedelta
from pathlib import Path
import tempfile

from PyQt6 import QtCore, QtGui, QtWidgets

from controllers.settings_controller import SettingsController
from controllers.report_controller import ReportController


try:
    from database.db import execute, fetch_all
except Exception:  # pragma: no cover - import guard for isolated UI previews.
    execute = None
    fetch_all = None


CAREPLUS_GREEN = "#00a651"
TEXT_DARK = "#0f172a"
TEXT_MUTED = "#64748b"
PAGE_BG = "#f8fafc"


def _safe_fetch_all(query, params=()):
    if fetch_all is None:
        return []
    try:
        return fetch_all(query, params) or []
    except Exception:
        return []


def _safe_execute(query, params=()):
    if execute is None:
        return False
    try:
        return bool(execute(query, params))
    except Exception:
        return False


def _hash_password(password):
    return hashlib.sha256(str(password or "").encode()).hexdigest()


def _as_text(value, default=""):
    if value is None:
        return default
    return str(value)


def _as_float(value):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _as_int(value):
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _is_active(row):
    value = row.get("is_active", True)
    if isinstance(value, str):
        return value.lower() not in {"0", "false", "no", "ngung", "inactive"}
    return bool(value)


def _contains(row, fields, query):
    if not query:
        return True
    normalized = query.lower().strip()
    return any(normalized in _as_text(row.get(field)).lower() for field in fields)


def _parse_date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = _as_text(value).strip()
    if not text:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y", "%d/%m/%Y %H:%M"):
        try:
            return datetime.strptime(text[:19], fmt).date()
        except ValueError:
            continue
    return None


def _format_date(value):
    parsed = _parse_date(value)
    if parsed:
        return parsed.strftime("%d/%m/%Y")
    return _as_text(value, "Chưa có")


def _format_datetime(value):
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y %H:%M")
    text = _as_text(value).strip()
    if not text:
        return "Chưa có"
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(text[:19], fmt).strftime("%d/%m/%Y %H:%M")
        except ValueError:
            continue
    return text


def _age_from_dob(value):
    dob = _parse_date(value)
    if not dob:
        return None
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def _format_money(value):
    return f"{_as_float(value):,.0f}".replace(",", ".") + " đ"


def _status_kind(text):
    lowered = _as_text(text).lower()
    if any(word in lowered for word in ("thành công", "hoạt động", "paid", "an toàn", "còn hàng")):
        return "success"
    if any(word in lowered for word in ("chờ", "pending", "tạm", "sắp hết", "đang")):
        return "warning"
    if any(word in lowered for word in ("lỗi", "thất bại", "hết hàng", "khóa", "ngừng", "nguy hiểm", "unpaid")):
        return "danger"
    return "neutral"


def _status_colors(kind):
    return {
        "success": ("#dcfce7", "#15803d"),
        "warning": ("#ffedd5", "#c2410c"),
        "danger": ("#fee2e2", "#b91c1c"),
        "info": ("#dbeafe", "#1d4ed8"),
        "neutral": ("#f1f5f9", "#475569"),
    }.get(kind, ("#f1f5f9", "#475569"))


ROLE_LABELS = {
    "admin": "Quản trị viên",
    "doctor": "Bác sĩ",
    "patient": "Khách hàng",
    "staff": "Nhân viên",
    "receptionist": "Lễ tân",
    "accountant": "Kế toán",
    "nurse": "Điều dưỡng",
}


ROLE_KIND = {
    "admin": "success",
    "doctor": "info",
    "receptionist": "warning",
    "accountant": "neutral",
    "nurse": "info",
    "staff": "neutral",
    "patient": "warning",
}


ACCOUNT_ROLE_OPTIONS = [
    ("Quản trị viên", "admin"),
    ("Bác sĩ", "doctor"),
    ("Lễ tân", "receptionist"),
    ("Kế toán", "accountant"),
    ("Điều dưỡng", "nurse"),
    ("Nhân viên", "staff"),
    ("Khách hàng", "patient"),
]


ROLE_DB_MAP = {
    "admin": "admin",
    "doctor": "doctor",
    "receptionist": "staff",
    "accountant": "staff",
    "nurse": "staff",
    "staff": "staff",
    "patient": "patient",
}


def _db_role(role):
    return ROLE_DB_MAP.get(_as_text(role).lower().strip(), _as_text(role).lower().strip())


def _role_label(role):
    key = _as_text(role).lower().strip()
    return ROLE_LABELS.get(key, _as_text(role).title())


class LineChartWidget(QtWidgets.QWidget):
    def __init__(self, labels=None, values=None, color=CAREPLUS_GREEN, parent=None):
        super().__init__(parent)
        self.labels = labels or []
        self.values = values or []
        self.color = QtGui.QColor(color)
        self.setMinimumHeight(230)

    def set_data(self, labels, values):
        self.labels = labels
        self.values = values
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        rect = self.rect().adjusted(16, 12, -16, -12)
        if not self.values:
            painter.setPen(QtGui.QColor(TEXT_MUTED))
            painter.drawText(rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Chưa có dữ liệu")
            return

        left, right, top, bottom = 48, 16, 18, 32
        chart = self.rect().adjusted(left, top, -right, -bottom)
        max_value = max(max(self.values), 1)
        painter.setPen(QtGui.QPen(QtGui.QColor("#edf2f7"), 1))
        for i in range(5):
            y = chart.top() + i * chart.height() / 4
            painter.drawLine(chart.left(), int(y), chart.right(), int(y))

        points = []
        step = chart.width() / max(1, len(self.values) - 1)
        for idx, value in enumerate(self.values):
            x = chart.left() + idx * step
            y = chart.bottom() - (float(value) / max_value * chart.height())
            points.append(QtCore.QPointF(x, y))

        area = QtGui.QPainterPath()
        area.moveTo(points[0].x(), chart.bottom())
        for point in points:
            area.lineTo(point)
        area.lineTo(points[-1].x(), chart.bottom())
        area.closeSubpath()
        gradient = QtGui.QLinearGradient(0, chart.top(), 0, chart.bottom())
        gradient.setColorAt(0, QtGui.QColor(self.color.red(), self.color.green(), self.color.blue(), 90))
        gradient.setColorAt(1, QtGui.QColor(self.color.red(), self.color.green(), self.color.blue(), 5))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(gradient)
        painter.drawPath(area)

        line = QtGui.QPainterPath()
        line.moveTo(points[0])
        for point in points[1:]:
            line.lineTo(point)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.setPen(QtGui.QPen(self.color, 3))
        painter.drawPath(line)
        painter.setBrush(QtGui.QColor("white"))
        for point in points:
            painter.drawEllipse(point, 4, 4)

        painter.setPen(QtGui.QColor(TEXT_MUTED))
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        for idx, label in enumerate(self.labels):
            x = chart.left() + idx * step - 14
            painter.drawText(int(x), self.height() - 10, _as_text(label)[:8])


class DonutChartWidget(QtWidgets.QWidget):
    COLORS = ["#00a651", "#2563eb", "#f97316", "#8b5cf6", "#ef4444", "#14b8a6"]

    def __init__(self, items=None, parent=None):
        super().__init__(parent)
        self.items = items or []
        self.setMinimumHeight(230)

    def set_items(self, items):
        self.items = items
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        if not self.items or sum(value for _, value in self.items) <= 0:
            painter.setPen(QtGui.QColor(TEXT_MUTED))
            painter.drawText(self.rect(), QtCore.Qt.AlignmentFlag.AlignCenter, "Chưa có dữ liệu")
            return

        total = sum(value for _, value in self.items)
        size = min(self.height() - 48, self.width() * 0.42)
        pie_rect = QtCore.QRectF(22, 32, size, size)
        start = 90 * 16
        for idx, (_, value) in enumerate(self.items):
            span = int(round(-(value / total) * 360 * 16))
            painter.setBrush(QtGui.QColor(self.COLORS[idx % len(self.COLORS)]))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawPie(pie_rect, start, span)
            start += span

        inner = pie_rect.adjusted(size * 0.28, size * 0.28, -size * 0.28, -size * 0.28)
        painter.setBrush(QtGui.QColor("white"))
        painter.drawEllipse(inner)

        x = int(pie_rect.right()) + 26
        y = 34
        painter.setFont(QtGui.QFont("Arial", 9))
        for idx, (label, value) in enumerate(self.items):
            color = QtGui.QColor(self.COLORS[idx % len(self.COLORS)])
            painter.setBrush(color)
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(x, y + idx * 28, 14, 14, 3, 3)
            painter.setPen(QtGui.QColor(TEXT_DARK))
            percent = value / total * 100
            painter.drawText(x + 22, y + 12 + idx * 28, f"{label}: {percent:.0f}%")


class FormDialog(QtWidgets.QDialog):
    def __init__(self, title, fields, data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(460)
        self.inputs = {}
        data = data or {}

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        form = QtWidgets.QFormLayout()
        form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        form.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(12)

        for field in fields:
            key = field["key"]
            value = data.get(key, field.get("default", ""))
            widget_type = field.get("type", "text")
            if widget_type == "combo":
                widget = QtWidgets.QComboBox()
                for label, item_value in field.get("options", []):
                    widget.addItem(label, item_value)
                index = widget.findData(value)
                if index < 0:
                    index = widget.findText(_as_text(value))
                widget.setCurrentIndex(max(index, 0))
            elif widget_type == "spin":
                widget = QtWidgets.QSpinBox()
                widget.setRange(field.get("min", 0), field.get("max", 100000000))
                widget.setValue(_as_int(value))
            elif widget_type == "money":
                widget = QtWidgets.QDoubleSpinBox()
                widget.setRange(0, 1000000000)
                widget.setDecimals(0)
                widget.setSuffix(" đ")
                widget.setValue(_as_float(value))
            elif widget_type == "date":
                widget = QtWidgets.QDateEdit()
                widget.setCalendarPopup(True)
                parsed = _parse_date(value) or date.today()
                widget.setDate(QtCore.QDate(parsed.year, parsed.month, parsed.day))
            elif widget_type == "password":
                widget = QtWidgets.QLineEdit(_as_text(value))
                widget.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            else:
                widget = QtWidgets.QLineEdit(_as_text(value))
            widget.setStyleSheet(self._input_style())
            self.inputs[key] = (widget, field)
            form.addRow(field["label"], widget)

        layout.addLayout(form)
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Save | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        buttons.button(QtWidgets.QDialogButtonBox.StandardButton.Save).setText("Lưu")
        buttons.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setText("Hủy")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    @staticmethod
    def _input_style():
        return """
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
                min-height: 36px;
                padding: 6px 10px;
                border: 1px solid #dbe3ef;
                border-radius: 8px;
                background: white;
                color: #0f172a;
                font-size: 13px;
            }
        """

    def values(self):
        payload = {}
        for key, (widget, field) in self.inputs.items():
            widget_type = field.get("type", "text")
            if widget_type == "combo":
                payload[key] = widget.currentData()
            elif widget_type == "spin":
                payload[key] = widget.value()
            elif widget_type == "money":
                payload[key] = widget.value()
            elif widget_type == "date":
                payload[key] = widget.date().toString("yyyy-MM-dd")
            else:
                payload[key] = widget.text().strip()
        return payload


class AdminBasePage(QtWidgets.QWidget):
    page_title = "Admin"
    breadcrumb = "Dashboard / Admin"

    def __init__(self, user_data=None, parent=None):
        super().__init__(parent)
        self.user_data = user_data or {}
        self.content_layout = QtWidgets.QVBoxLayout(self)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(18)

    def _card(self):
        card = QtWidgets.QFrame()
        card.setObjectName("adminCard")
        card.setStyleSheet("""
            QFrame#adminCard {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
            }
        """)
        shadow = QtWidgets.QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(18)
        shadow.setOffset(0, 3)
        shadow.setColor(QtGui.QColor(15, 23, 42, 18))
        card.setGraphicsEffect(shadow)
        return card

    def _section_title(self, text):
        label = QtWidgets.QLabel(text)
        label.setStyleSheet("font-size: 17px; font-weight: 900; color: #0f172a; background: transparent;")
        return label

    def _muted(self, text):
        label = QtWidgets.QLabel(text)
        label.setWordWrap(True)
        label.setStyleSheet("font-size: 12px; font-weight: 600; color: #64748b; background: transparent;")
        return label

    def _filter_field(self, label_text, field):
        wrapper = QtWidgets.QWidget()
        wrapper.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        layout = QtWidgets.QVBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        label = QtWidgets.QLabel(label_text)
        label.setStyleSheet("font-size: 11px; font-weight: 850; color: #64748b; background: transparent;")
        layout.addWidget(label)
        layout.addWidget(field)
        return wrapper

    def _button(self, text, primary=False, danger=False):
        btn = QtWidgets.QPushButton(text)
        btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        if primary:
            style = "background: #00a651; color: white; border: 1px solid #00a651;"
        elif danger:
            style = "background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca;"
        else:
            style = "background: white; color: #0f172a; border: 1px solid #dbe3ef;"
        btn.setStyleSheet(f"""
            QPushButton {{
                {style}
                min-height: 36px;
                padding: 0 12px;
                border-radius: 8px;
                font-weight: 800;
                font-size: 13px;
            }}
            QPushButton:hover {{ background: #f8fafc; }}
            QPushButton:disabled {{ background: #e5e7eb; color: #94a3b8; border-color: #e5e7eb; }}
        """)
        return btn

    def _icon_button(self, text, kind="info"):
        bg, color = _status_colors({"info": "info", "danger": "danger", "success": "success"}.get(kind, "neutral"))
        icon_text = {
            "Xem": "◉",
            "Sửa": "✎",
            "Xóa": "⌫",
            "In": "⎙",
            "Khóa": "🔒",
            "Mở": "🔓",
            "Tải": "⇩",
            "Đổi": "⋯",
            "•••": "⋯",
            "Hủy": "×",
        }.get(text, text)
        btn = QtWidgets.QPushButton(icon_text)
        btn.setToolTip(text)
        btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        btn.setFixedSize(30, 30)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {bg};
                color: {color};
                border: none;
                border-radius: 7px;
                padding: 0 9px;
                font-weight: 900;
            }}
        """)
        return btn

    def _badge(self, text, kind=None):
        kind = kind or _status_kind(text)
        bg, color = _status_colors(kind)
        label = QtWidgets.QLabel(text)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        label.setMinimumHeight(24)
        label.setMaximumHeight(28)
        label.setStyleSheet(f"""
            QLabel {{
                background: {bg};
                color: {color};
                border-radius: 10px;
                padding: 4px 10px;
                font-size: 12px;
                font-weight: 900;
            }}
        """)
        return label

    def _stat_card(self, icon, label, value, hint, color="#2563eb"):
        card = self._card()
        card.setMinimumHeight(118)
        card.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        icon_label = QtWidgets.QLabel(icon)
        icon_label.setFixedSize(48, 48)
        icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(f"background: {color}; color: white; border-radius: 12px; font-size: 21px;")
        text_layout = QtWidgets.QVBoxLayout()
        text_layout.setSpacing(4)
        title = QtWidgets.QLabel(label)
        title.setWordWrap(True)
        title.setStyleSheet("font-size: 12px; color: #1e293b; font-weight: 850; background: transparent;")
        val = QtWidgets.QLabel(_as_text(value))
        value_size = 20 if len(_as_text(value)) > 10 else 26
        val.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        val.setStyleSheet(f"font-size: {value_size}px; color: {TEXT_DARK}; font-weight: 950; background: transparent;")
        small = QtWidgets.QLabel(hint)
        small.setWordWrap(True)
        small.setStyleSheet("font-size: 11px; color: #64748b; font-weight: 700; background: transparent;")
        text_layout.addWidget(title)
        text_layout.addWidget(val)
        text_layout.addWidget(small)
        layout.addWidget(icon_label)
        layout.addLayout(text_layout)
        layout.addStretch()
        return card

    def _action_cell(self, buttons):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(6)
        for button in buttons:
            layout.addWidget(button)
        layout.addStretch()
        return widget

    def _style_table(self, table, font_size=12):
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.setAlternatingRowColors(False)
        table.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        table.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        table.horizontalHeader().setMinimumSectionSize(28)
        table.setStyleSheet(f"""
            QTableWidget {{
                background: white;
                border: 1px solid #edf2f7;
                border-radius: 10px;
                color: #0f172a;
                font-size: {font_size}px;
            }}
            QHeaderView::section {{
                background: #f8fafc;
                color: #475569;
                padding: 8px 4px;
                border: none;
                border-bottom: 1px solid #e2e8f0;
                font-weight: 900;
            }}
            QTableWidget::item {{
                padding: 5px 4px;
                border-bottom: 1px solid #f1f5f9;
            }}
            QScrollBar {{ width: 0px; height: 0px; }}
        """)

    def _show_info(self, title, message):
        QtWidgets.QMessageBox.information(self, title, message)

    def _confirm(self, title, message):
        result = QtWidgets.QMessageBox.question(
            self,
            title,
            message,
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No,
        )
        return result == QtWidgets.QMessageBox.StandardButton.Yes


class AdminListPage(AdminBasePage):
    headers = []
    column_widths = []
    search_placeholder = "Tìm kiếm..."
    search_min_width = 190
    search_max_width = 360
    filter_combo_width = 132
    page_size_options = [10, 20, 50, 100]

    def __init__(self, user_data=None, parent=None):
        self.current_page = 1
        self.page_size = 10
        self.rows = []
        self.filtered_rows = []
        super().__init__(user_data, parent)
        self._build_list_page()
        self.refresh()

    def _build_list_page(self):
        self.stats_row = QtWidgets.QHBoxLayout()
        self.stats_row.setSpacing(12)
        self.content_layout.addLayout(self.stats_row)

        filter_card = self._card()
        filter_layout = QtWidgets.QHBoxLayout(filter_card)
        filter_layout.setContentsMargins(16, 14, 16, 14)
        filter_layout.setSpacing(10)
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText(self.search_placeholder)
        self.search_input.setMinimumHeight(38)
        self.search_input.setMinimumWidth(self.search_min_width)
        self.search_input.setMaximumWidth(self.search_max_width)
        self.search_input.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.search_input.setStyleSheet(FormDialog._input_style())
        self.search_input.textChanged.connect(self._reset_and_refresh)
        filter_layout.addWidget(self.search_input, 1)
        self._add_filters(filter_layout)
        filter_layout.addStretch()
        self._add_toolbar_buttons(filter_layout)
        self.content_layout.addWidget(filter_card)

        table_card = self._card()
        table_layout = QtWidgets.QVBoxLayout(table_card)
        table_layout.setContentsMargins(16, 16, 16, 16)
        table_layout.setSpacing(12)
        title_row = QtWidgets.QHBoxLayout()
        title_row.addWidget(self._section_title(self.table_title()))
        title_row.addStretch()
        self.total_label = QtWidgets.QLabel()
        self.total_label.setStyleSheet("color: #64748b; font-weight: 800;")
        title_row.addWidget(self.total_label)
        table_layout.addLayout(title_row)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setWordWrap(False)
        self.table.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setAlternatingRowColors(False)
        self.table.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setMinimumSectionSize(22)
        self.table.horizontalHeader().setDefaultSectionSize(90)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #edf2f7;
                border-radius: 10px;
                color: #0f172a;
                font-size: 12px;
            }
            QHeaderView::section {
                background: #f8fafc;
                color: #475569;
                padding: 8px 4px;
                border: none;
                border-bottom: 1px solid #e2e8f0;
                font-weight: 900;
            }
            QTableWidget::item {
                padding: 5px 4px;
                border-bottom: 1px solid #f1f5f9;
            }
            QScrollBar { width: 0px; height: 0px; }
        """)
        table_layout.addWidget(self.table)

        pager = QtWidgets.QHBoxLayout()
        pager.setSpacing(8)
        pager.addWidget(QtWidgets.QLabel("Hiển thị"))
        self.page_size_combo = QtWidgets.QComboBox()
        self.page_size_combo.addItems([str(v) for v in self.page_size_options])
        self.page_size_combo.setFixedWidth(72)
        self.page_size_combo.setStyleSheet(FormDialog._input_style())
        self.page_size_combo.currentTextChanged.connect(self._page_size_changed)
        pager.addWidget(self.page_size_combo)
        pager.addWidget(QtWidgets.QLabel("bản ghi"))
        pager.addStretch()
        self.prev_btn = self._button("‹")
        self.prev_btn.setFixedWidth(38)
        self.prev_btn.clicked.connect(self._prev_page)
        self.page_label = QtWidgets.QLabel()
        self.page_label.setStyleSheet("font-weight: 900; color: #0f172a;")
        self.next_btn = self._button("›")
        self.next_btn.setFixedWidth(38)
        self.next_btn.clicked.connect(self._next_page)
        pager.addWidget(self.prev_btn)
        pager.addWidget(self.page_label)
        pager.addWidget(self.next_btn)
        table_layout.addLayout(pager)
        self.content_layout.addWidget(table_card)
        self.content_layout.addStretch()

    def table_title(self):
        return self.page_title

    def _combo(self, items):
        combo = QtWidgets.QComboBox()
        for label, value in items:
            combo.addItem(label, value)
        combo.setMinimumHeight(38)
        combo.setFixedWidth(self.filter_combo_width)
        combo.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        combo.setStyleSheet(FormDialog._input_style())
        combo.currentIndexChanged.connect(self._reset_and_refresh)
        return combo

    def _add_filters(self, layout):
        return

    def _add_toolbar_buttons(self, layout):
        export_btn = self._button("Xuất Excel")
        export_btn.setFixedWidth(106)
        export_btn.clicked.connect(self.export_excel)
        layout.addWidget(export_btn)

    def _reset_and_refresh(self):
        self.current_page = 1
        self.refresh()

    def _page_size_changed(self, value):
        self.page_size = int(value)
        self.current_page = 1
        self._render_table()

    def _prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self._render_table()

    def _next_page(self):
        total_pages = max(1, (len(self.filtered_rows) + self.page_size - 1) // self.page_size)
        if self.current_page < total_pages:
            self.current_page += 1
            self._render_table()

    def refresh(self):
        self.rows = self.load_rows()
        self.filtered_rows = [row for row in self.rows if self.accept_row(row)]
        self._render_stats()
        self._render_table()

    def load_rows(self):
        return []

    def accept_row(self, row):
        return True

    def stat_cards(self):
        return []

    def _render_stats(self):
        while self.stats_row.count():
            item = self.stats_row.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        for card in self.stat_cards():
            self.stats_row.addWidget(card)
        self.stats_row.addStretch()

    def _render_table(self):
        total_pages = max(1, (len(self.filtered_rows) + self.page_size - 1) // self.page_size)
        self.current_page = min(max(1, self.current_page), total_pages)
        start = (self.current_page - 1) * self.page_size
        visible = self.filtered_rows[start:start + self.page_size]
        self.table.setRowCount(len(visible))
        for row_index, row_data in enumerate(visible):
            self.render_row(row_index, row_data)
        self.total_label.setText(f"{len(self.filtered_rows)} bản ghi")
        self.page_label.setText(f"Trang {self.current_page}/{total_pages}")
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)
        self.table.resizeRowsToContents()
        for row in range(self.table.rowCount()):
            self.table.setRowHeight(row, max(self.table.rowHeight(row), 44))
        self._apply_column_widths()
        target_rows = max(len(visible), min(self.page_size, 10))
        self.table.setFixedHeight(42 + target_rows * 44 + 4)

    def _apply_column_widths(self):
        column_count = self.table.columnCount()
        ratios = self.column_widths if len(self.column_widths) == column_count else [1] * column_count
        available = max(self.table.viewport().width() - 4, column_count * 28)
        ratio_total = sum(ratios) or 1
        used = 0
        for column, ratio in enumerate(ratios):
            if column == column_count - 1:
                width = max(28, available - used)
            else:
                width = max(28, int(available * ratio / ratio_total))
                used += width
            self.table.setColumnWidth(column, width)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "table"):
            QtCore.QTimer.singleShot(0, self._apply_column_widths)

    def render_row(self, row_index, row_data):
        return

    def _set_item(self, row, column, text):
        item = QtWidgets.QTableWidgetItem(_as_text(text))
        item.setForeground(QtGui.QColor(TEXT_DARK))
        self.table.setItem(row, column, item)

    def _action_cell(self, buttons):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(6)
        for button in buttons:
            layout.addWidget(button)
        layout.addStretch()
        return widget

    def export_excel(self):
        import xml.sax.saxutils as saxutils
        import tempfile
        import zipfile
        import shutil

        default_name = f"{self.page_title.lower().replace(' ', '_')}_{datetime.now().strftime('%Y_%m_%d')}.xlsx"
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Xuất Excel", default_name, "Excel Files (*.xlsx)")
        if not path:
            return
        if not path.lower().endswith(".xlsx"):
            path += ".xlsx"

        def make_row_xml(index, values):
            cells = []
            for col_idx, val in enumerate(values):
                col_letter = chr(65 + col_idx) if col_idx < 26 else f"{chr(64 + col_idx // 26)}{chr(65 + col_idx % 26)}"
                cell_ref = f"{col_letter}{index}"
                str_val = _as_text(val)
                escaped = saxutils.escape(str_val)
                cells.append(f'<c r="{cell_ref}" t="inlineStr"><is><t>{escaped}</t></is></c>')
            return f'<row r="{index}">' + "".join(cells) + "</row>"

        export_headers = getattr(self, "export_headers", self.headers)
        rows_xml = [make_row_xml(1, export_headers)]
        for i, row in enumerate(self.filtered_rows, start=2):
            rows_xml.append(make_row_xml(i, self.export_row(row)))

        sheet_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<sheetData>' + "".join(rows_xml) + "</sheetData>"
            '</worksheet>'
        )

        workbook_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets>'
            '</workbook>'
        )

        content_types_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '</Types>'
        )

        root_rels_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '</Relationships>'
        )

        workbook_rels_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
            '</Relationships>'
        )

        try:
            tmp_fd, tmp_path = tempfile.mkstemp(suffix=".xlsx")
            os.close(tmp_fd)
            with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("[Content_Types].xml", content_types_xml)
                zf.writestr("_rels/.rels", root_rels_xml)
                zf.writestr("xl/workbook.xml", workbook_xml)
                zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml)
                zf.writestr("xl/worksheets/sheet1.xml", sheet_xml)
            shutil.copy2(tmp_path, path)
            os.unlink(tmp_path)
            self._show_info("Xuất Excel", "Đã xuất dữ liệu ra file Excel thành công.")
        except Exception as e:
            self._show_info("Lỗi xuất Excel", f"Không thể tạo file Excel: {e}")

    def export_row(self, row):
        return [_as_text(row.get(header.lower(), "")) for header in self.headers]


class AdminHomePage(AdminBasePage):
    page_title = "Dashboard Admin"
    breadcrumb = "Tổng quan hệ thống quản trị"

    def __init__(self, user_data=None, parent=None):
        super().__init__(user_data, parent)
        self.refresh()

    def refresh(self):
        patients = _safe_fetch_all("SELECT * FROM Patients")
        doctors = _safe_fetch_all("SELECT * FROM Doctors")
        notifications = _safe_fetch_all(
            """
            SELECT title, content, created_at
            FROM Notifications
            ORDER BY created_at DESC
            LIMIT 4
            """
        )
        payments = _safe_fetch_all(
            """
            SELECT p.*, s.service_name
            FROM Payments p
            LEFT JOIN Appointments a ON a.appointment_id = p.appointment_id
            LEFT JOIN Invoices i ON i.payment_id = p.payment_id
            LEFT JOIN Services s ON s.service_id = i.service_id
            ORDER BY p.payment_date DESC
            """
        )
        appointments = _safe_fetch_all(
            """
            SELECT a.*, pa.name AS patient_name, s.service_name AS service
            FROM Appointments a
            LEFT JOIN Patients pa ON pa.patient_id = a.patient_id
            LEFT JOIN Invoices i ON i.payment_id = (
                SELECT p2.payment_id
                FROM Payments p2
                WHERE p2.appointment_id = a.appointment_id
                ORDER BY p2.payment_date DESC
                LIMIT 1
            )
            LEFT JOIN Services s ON s.service_id = i.service_id
            ORDER BY a.appointment_date DESC
            """
        )
        prescriptions = _safe_fetch_all("SELECT * FROM Prescriptions")

        top = QtWidgets.QHBoxLayout()
        top.setSpacing(16)
        top.addWidget(self._stat_card("👥", "Tổng bệnh nhân", len(patients), "Dữ liệu theo DB hiện tại", "#2563eb"))
        top.addWidget(self._stat_card("🩺", "Tổng bác sĩ", len(doctors), "Dữ liệu theo DB hiện tại", "#00a651"))
        top.addWidget(self._stat_card("📅", "Tổng lịch hẹn", len(appointments), "Dữ liệu theo DB hiện tại", "#f97316"))
        today = datetime.now().date()
        today_rx = sum(1 for item in prescriptions if _parse_date(item.get("updated_at") or item.get("dispensed_at")) == today)
        top.addWidget(self._stat_card("📋", "Đơn thuốc hôm nay", today_rx, "Dữ liệu theo DB hiện tại", "#8b5cf6"))
        self.content_layout.addLayout(top)

        chart_row = QtWidgets.QHBoxLayout()
        chart_row.setSpacing(16)
        chart_card = self._card()
        chart_layout = QtWidgets.QVBoxLayout(chart_card)
        chart_layout.setContentsMargins(18, 18, 18, 18)
        chart_layout.addWidget(self._section_title("Lượt khám bệnh hằng tuần"))
        labels, values = self._weekly_appointment_data(appointments)
        chart_layout.addWidget(LineChartWidget(labels, values))
        chart_row.addWidget(chart_card, 2)

        chart_row.addWidget(self._revenue_panel(payments), 1)
        self.content_layout.addLayout(chart_row)

        bottom = QtWidgets.QHBoxLayout()
        bottom.setSpacing(16)
        bottom.addWidget(self._appointments_panel(appointments), 1)
        bottom.addWidget(self._notifications_panel(notifications), 1)
        bottom.addWidget(self._quick_stats_panel(patients, doctors, appointments, prescriptions), 1)
        self.content_layout.addLayout(bottom)
        self.content_layout.addStretch()

    def _weekly_appointment_data(self, appointments):
        today = datetime.now().date()
        start = today - timedelta(days=today.weekday())
        labels = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
        values = []
        for offset in range(7):
            current = start + timedelta(days=offset)
            values.append(sum(1 for item in appointments if _parse_date(item.get("appointment_date")) == current))
        return labels, values

    def _revenue_panel(self, payments):
        card = self._card()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(11)
        layout.addWidget(self._section_title("Tổng quan doanh thu"))
        total = sum(_as_float(p.get("total_amount")) for p in payments if p.get("status") == "paid")
        value = QtWidgets.QLabel(_format_money(total).replace(" VND", " đ"))
        value.setStyleSheet("font-size: 27px; font-weight: 950; color: #00a651;")
        layout.addWidget(value)
        layout.addWidget(self._muted("Chỉ tính các giao dịch đã thanh toán"))
        items = [("Doanh thu đã thanh toán", total, "100%", "#00a651")]
        for label, amount, percent, color in items:
            row = QtWidgets.QHBoxLayout()
            dot = QtWidgets.QLabel()
            dot.setFixedSize(9, 9)
            dot.setStyleSheet(f"background: {color}; border-radius: 4px;")
            row.addWidget(dot)
            row.addWidget(self._muted(label))
            row.addStretch()
            row.addWidget(self._muted(_format_money(amount).replace(" VND", " đ")))
            row.addWidget(self._muted(percent))
            layout.addLayout(row)
        layout.addStretch()
        return card

    def _appointments_panel(self, appointments):
        card = self._card()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.addWidget(self._section_title("Lịch hẹn sắp tới"))
        upcoming = sorted(
            [a for a in appointments if (_parse_date(a.get("appointment_date")) or date.min) >= date.today()],
            key=lambda item: _as_text(item.get("appointment_date")),
        )[:5]
        if not upcoming:
            layout.addWidget(self._muted("Chưa có lịch hẹn sắp tới"))
            layout.addStretch()
            return card
        for item in upcoming:
            layout.addWidget(self._muted(f"{item.get('patient_name', 'Bệnh nhân')} - {item.get('service', 'Khám bệnh')} - {_format_datetime(item.get('appointment_date'))}"))
        layout.addStretch()
        return card

    def _notifications_panel(self, notifications):
        card = self._card()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.addWidget(self._section_title("Thông báo hệ thống"))
        if not notifications:
            layout.addWidget(self._muted("Chưa có thông báo hệ thống"))
            layout.addStretch()
            return card
        for item in notifications:
            text = _as_text(item.get("title"), "Thông báo")
            detail = _as_text(item.get("content"), "")
            row = QtWidgets.QHBoxLayout()
            row.addWidget(self._badge(text, _status_kind(text)))
            row.addStretch()
            layout.addLayout(row)
            if detail:
                layout.addWidget(self._muted(detail))
        layout.addStretch()
        return card

    def _quick_stats_panel(self, patients, doctors, appointments, prescriptions):
        card = self._card()
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.addWidget(self._section_title("Thống kê nhanh"))
        today = date.today()
        new_patients = sum(1 for item in patients if _parse_date(item.get("created_at")) == today)
        active_doctors = sum(1 for item in doctors if _is_active(item))
        done = sum(1 for item in appointments if item.get("status") == "done")
        dispensed = sum(1 for item in prescriptions if item.get("status") == "dispensed")
        for label, value in [
            ("Bệnh nhân mới", new_patients),
            ("Bác sĩ hoạt động", active_doctors),
            ("Lịch hẹn hoàn thành", done),
            ("Đơn thuốc đã phát", dispensed),
        ]:
            row = QtWidgets.QHBoxLayout()
            row.addWidget(QtWidgets.QLabel(label))
            row.addStretch()
            row.addWidget(self._badge(str(value), "info"))
            layout.addLayout(row)
        layout.addStretch()
        return card


class AccountManagementPage(AdminListPage):
    page_title = "Quản lý tài khoản"
    breadcrumb = "Dashboard / Quản lý tài khoản"
    headers = ["☐", "STT", "Họ và tên", "Email", "Số điện thoại", "Vai trò", "Trạng thái", "Ngày tạo", "Thao tác"]
    column_widths = [0.35, 0.45, 1.55, 2.0, 1.25, 1.25, 1.25, 1.35, 0.95]
    search_placeholder = "Tìm kiếm tài khoản (Tên, Email, SĐT...)"

    def __init__(self, user_data=None, parent=None):
        self.selected_user_ids = set()
        self._header_checkbox = None
        self.load_error = ""
        self._is_loading = False
        self._suspend_checkbox_sync = False
        self.empty_card = None
        self.empty_label = None
        self.clear_filter_btn = None
        self.retry_btn = None
        self.table_card = None
        self._current_page_rows = []
        self._search_debounce_timer = None
        super().__init__(user_data, parent)

    def _add_filters(self, layout):
        self.role_filter = self._combo([("Tất cả vai trò", "all")] + ACCOUNT_ROLE_OPTIONS)
        self.status_filter = self._combo([
            ("Tất cả trạng thái", "all"),
            ("Hoạt động", "active"),
            ("Bị khóa", "locked"),
            ("Đã xóa mềm", "deleted"),
        ])
        layout.addWidget(self.role_filter)
        layout.addWidget(self.status_filter)

    def _add_toolbar_buttons(self, layout):
        add_btn = self._button("Thêm tài khoản", primary=True)
        add_btn.setFixedWidth(132)
        add_btn.clicked.connect(self.add_account)
        layout.addWidget(add_btn)
        export_btn = self._button("Xuất Excel")
        export_btn.setFixedWidth(106)
        export_btn.clicked.connect(self.export_excel)
        layout.addWidget(export_btn)

    def _build_list_page(self):
        super()._build_list_page()
        self.search_input.textChanged.disconnect()
        self._search_debounce_timer = QtCore.QTimer(self)
        self._search_debounce_timer.setSingleShot(True)
        self._search_debounce_timer.timeout.connect(self._reset_and_refresh)
        self.search_input.textChanged.connect(self._on_search_text_changed)
        self.table_card = self.table.parentWidget().parentWidget()
        self.bulk_row = QtWidgets.QHBoxLayout()
        self.bulk_row.setSpacing(8)
        self.bulk_label = QtWidgets.QLabel("Chưa chọn tài khoản")
        self.bulk_label.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 800;")
        self.bulk_row.addWidget(self.bulk_label)
        self.bulk_row.addStretch()

        self.bulk_lock_btn = self._button("Khóa", danger=True)
        self.bulk_unlock_btn = self._button("Mở khóa", primary=True)
        self.bulk_delete_btn = self._button("Xóa", danger=True)
        self.bulk_export_btn = self._button("Xuất Excel")
        self.bulk_assign_btn = self._button("Gán vai trò")
        for btn in [self.bulk_lock_btn, self.bulk_unlock_btn, self.bulk_delete_btn, self.bulk_assign_btn, self.bulk_export_btn]:
            btn.setVisible(False)
            self.bulk_row.addWidget(btn)

        self.bulk_lock_btn.clicked.connect(lambda: self._apply_bulk_status(0))
        self.bulk_unlock_btn.clicked.connect(lambda: self._apply_bulk_status(1))
        self.bulk_delete_btn.clicked.connect(self._bulk_soft_delete)
        self.bulk_assign_btn.clicked.connect(self._bulk_assign_role)
        self.bulk_export_btn.clicked.connect(self._export_selected_excel)

        self.table_card.layout().insertLayout(1, self.bulk_row)

        self.empty_card = self._card()
        empty_layout = QtWidgets.QVBoxLayout(self.empty_card)
        empty_layout.setContentsMargins(24, 24, 24, 24)
        empty_layout.setSpacing(10)
        empty_icon = QtWidgets.QLabel("📭")
        empty_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        empty_icon.setStyleSheet("font-size: 34px;")
        self.empty_label = QtWidgets.QLabel("Không tìm thấy tài khoản phù hợp.")
        self.empty_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet("font-size: 14px; font-weight: 800; color: #475569;")
        action_row = QtWidgets.QHBoxLayout()
        action_row.addStretch()
        self.clear_filter_btn = self._button("Xóa bộ lọc")
        self.clear_filter_btn.clicked.connect(self._clear_filters)
        self.retry_btn = self._button("Thử lại", primary=True)
        self.retry_btn.clicked.connect(self.refresh)
        action_row.addWidget(self.clear_filter_btn)
        action_row.addWidget(self.retry_btn)
        action_row.addStretch()
        empty_layout.addWidget(empty_icon)
        empty_layout.addWidget(self.empty_label)
        empty_layout.addLayout(action_row)
        self.content_layout.insertWidget(2, self.empty_card)
        self.empty_card.hide()

    def _clear_filters(self):
        self.search_input.clear()
        self.role_filter.setCurrentIndex(0)
        self.status_filter.setCurrentIndex(0)
        self._reset_and_refresh()

    def _on_search_text_changed(self):
        if self._search_debounce_timer is not None:
            self._search_debounce_timer.start(350)

    def _reset_and_refresh(self):
        self.current_page = 1
        self.selected_doctor_ids.clear()
        self.refresh()

    def _set_loading(self, loading):
        self._is_loading = loading
        if hasattr(self, "search_input"):
            self.search_input.setEnabled(not loading)
        if hasattr(self, "role_filter"):
            self.role_filter.setEnabled(not loading)
        if hasattr(self, "status_filter"):
            self.status_filter.setEnabled(not loading)
        if hasattr(self, "page_size_combo"):
            self.page_size_combo.setEnabled(not loading)
        if loading:
            self.table.setRowCount(4)
            for row in range(4):
                for col in range(self.table.columnCount()):
                    self.table.setItem(row, col, QtWidgets.QTableWidgetItem("Đang tải..."))

    def _sync_bulk_ui(self):
        selected_count = len(self.selected_user_ids)
        has_selected = selected_count > 0
        self.bulk_label.setText(f"Đã chọn {selected_count} tài khoản" if has_selected else "Chưa chọn tài khoản")
        for btn in [self.bulk_lock_btn, self.bulk_unlock_btn, self.bulk_delete_btn, self.bulk_assign_btn, self.bulk_export_btn]:
            btn.setVisible(has_selected)

    def load_rows(self):
        self._set_loading(True)
        self.load_error = ""
        _safe_execute("ALTER TABLE Users ADD COLUMN deleted_at DATETIME NULL")
        try:
            if fetch_all is None:
                return []
            rows = fetch_all(
                """
                SELECT
                    u.user_id,
                    u.username,
                    u.role,
                    u.is_active,
                    u.created_at,
                    u.deleted_at,
                    COALESCE(d.name, p.name, u.username) AS full_name,
                    COALESCE(d.email, p.email, '') AS email,
                    COALESCE(d.phone, p.phone, '') AS phone,
                    COALESCE(us.avatar_path, '') AS avatar_path,
                    us.updated_at AS profile_updated_at
                FROM Users u
                LEFT JOIN Doctors d ON d.user_id = u.user_id
                LEFT JOIN Patients p ON p.user_id = u.user_id
                LEFT JOIN UserSettings us ON us.user_id = u.user_id
                ORDER BY u.user_id DESC
                """
            ) or []
            return rows
        except Exception as exc:
            self.load_error = f"Lỗi tải dữ liệu: {exc}"
            return []
        finally:
            self._set_loading(False)

    def accept_row(self, row):
        selected_role = self.role_filter.currentData()
        role_ok = selected_role == "all" or _db_role(row.get("role")) == _db_role(selected_role)
        deleted = bool(row.get("deleted_at"))
        status = "deleted" if deleted else ("active" if _is_active(row) else "locked")
        status_ok = self.status_filter.currentData() == "all" or status == self.status_filter.currentData()
        return role_ok and status_ok and _contains(row, ["username", "full_name", "email", "phone", "role"], self.search_input.text())

    def stat_cards(self):
        active = sum(1 for row in self.rows if _is_active(row) and not row.get("deleted_at"))
        locked = sum(1 for row in self.rows if not _is_active(row) and not row.get("deleted_at"))
        roles = len({row.get("role") for row in self.rows if row.get("role")})
        return [
            self._stat_card("👥", "Tổng tài khoản", len(self.rows), "Dữ liệu theo DB hiện tại", "#2563eb"),
            self._stat_card("👤", "Tài khoản hoạt động", active, "Dữ liệu theo DB hiện tại", "#00a651"),
            self._stat_card("🔒", "Tài khoản bị khóa", locked, "Dữ liệu theo DB hiện tại", "#f97316"),
            self._stat_card("🛡", "Vai trò hệ thống", roles, "Quản lý vai trò", "#8b5cf6"),
        ]

    def render_row(self, row, data):
        checkbox = QtWidgets.QCheckBox()
        checkbox.setChecked(data.get("user_id") in self.selected_user_ids)
        checkbox.stateChanged.connect(lambda state, user_id=data.get("user_id"): self._toggle_selected(user_id, state))
        check_wrap = QtWidgets.QWidget()
        check_layout = QtWidgets.QHBoxLayout(check_wrap)
        check_layout.setContentsMargins(0, 0, 0, 0)
        check_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        check_layout.addWidget(checkbox)
        self.table.setCellWidget(row, 0, check_wrap)
        self._set_item(row, 1, row + 1)
        display_name = _as_text(data.get("full_name") or data.get("username")).strip()
        initial = display_name[0].upper() if display_name else "?"
        self._set_item(row, 2, f"[{initial}] {display_name}")
        self._set_item(row, 3, data.get("email"))
        self._set_item(row, 4, data.get("phone"))
        role_key = _as_text(data.get("role")).lower().strip()
        self.table.setCellWidget(row, 5, self._badge(_role_label(role_key), ROLE_KIND.get(role_key, "info")))
        if data.get("deleted_at"):
            status_text = "Đã xóa mềm"
            status_kind = "neutral"
        else:
            status_text = "Hoạt động" if _is_active(data) else "Bị khóa"
            status_kind = "success" if _is_active(data) else "danger"
        self.table.setCellWidget(row, 6, self._badge(status_text, status_kind))
        self._set_item(row, 7, _format_datetime(data.get("created_at")))
        lock_text = "Khóa" if _is_active(data) else "Mở"
        view_btn = self._icon_button("Xem", "info")
        edit_btn = self._icon_button("Sửa", "info")
        lock_btn = self._icon_button(lock_text, "danger" if _is_active(data) else "success")
        delete_btn = self._icon_button("Xóa", "danger")
        reset_btn = self._icon_button("Đổi", "success")
        view_btn.clicked.connect(lambda _, item=data: self.view_account(item))
        edit_btn.clicked.connect(lambda _, item=data: self.edit_account(item))
        lock_btn.clicked.connect(lambda _, item=data: self.toggle_account(item))
        delete_btn.clicked.connect(lambda _, item=data: self.soft_delete_account(item))
        reset_btn.clicked.connect(lambda _, item=data: self.reset_password(item))
        self.table.setCellWidget(row, 8, self._action_cell([view_btn, edit_btn, lock_btn, reset_btn, delete_btn]))

    def _toggle_selected(self, user_id, state):
        if self._suspend_checkbox_sync:
            return
        if not user_id:
            return
        if state == int(QtCore.Qt.CheckState.Checked):
            self.selected_user_ids.add(user_id)
        else:
            self.selected_user_ids.discard(user_id)
        self._sync_bulk_ui()
        self._sync_header_checkbox()

    def _sync_header_checkbox(self):
        if not self._header_checkbox:
            return
        page_ids = [row.get("user_id") for row in self._current_page_rows if row.get("user_id")]
        if not page_ids:
            self._header_checkbox.setCheckState(QtCore.Qt.CheckState.Unchecked)
            return
        selected_in_page = sum(1 for user_id in page_ids if user_id in self.selected_user_ids)
        self._header_checkbox.blockSignals(True)
        if selected_in_page == 0:
            self._header_checkbox.setCheckState(QtCore.Qt.CheckState.Unchecked)
        elif selected_in_page == len(page_ids):
            self._header_checkbox.setCheckState(QtCore.Qt.CheckState.Checked)
        else:
            self._header_checkbox.setCheckState(QtCore.Qt.CheckState.PartiallyChecked)
        self._header_checkbox.blockSignals(False)

    def _toggle_select_page(self, state):
        page_ids = [row.get("user_id") for row in self._current_page_rows if row.get("user_id")]
        if state == int(QtCore.Qt.CheckState.Checked):
            for user_id in page_ids:
                self.selected_user_ids.add(user_id)
        elif state == int(QtCore.Qt.CheckState.Unchecked):
            for user_id in page_ids:
                self.selected_user_ids.discard(user_id)
        self._render_table()
        self._sync_bulk_ui()

    def _render_table(self):
        total_pages = max(1, (len(self.filtered_rows) + self.page_size - 1) // self.page_size)
        self.current_page = min(max(1, self.current_page), total_pages)
        start = (self.current_page - 1) * self.page_size
        visible = self.filtered_rows[start:start + self.page_size]
        self._current_page_rows = visible
        self.table.setRowCount(len(visible))
        for row_index, row_data in enumerate(visible):
            self.render_row(row_index, row_data)
        self.total_label.setText(f"{len(self.filtered_rows)} bản ghi")
        self.page_label.setText(f"Trang {self.current_page}/{total_pages}")
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)
        self.table.resizeRowsToContents()
        for row in range(self.table.rowCount()):
            self.table.setRowHeight(row, max(self.table.rowHeight(row), 44))
        self._apply_column_widths()
        target_rows = max(len(visible), min(self.page_size, 10))
        self.table.setFixedHeight(42 + target_rows * 44 + 4)

        self._setup_header_checkbox()
        self._sync_header_checkbox()
        self._sync_bulk_ui()
        self._update_empty_state()

    def _setup_header_checkbox(self):
        header = self.table.horizontalHeader()
        if self._header_checkbox is not None:
            self._header_checkbox.deleteLater()
            self._header_checkbox = None
        box = QtWidgets.QCheckBox(header)
        box.setTristate(True)
        box.stateChanged.connect(self._toggle_select_page)
        box.show()
        self._header_checkbox = box
        self._position_header_checkbox()

    def _position_header_checkbox(self):
        if not self._header_checkbox:
            return
        header = self.table.horizontalHeader()
        geo = header.sectionPosition(0)
        self._header_checkbox.move(geo + max(0, int(header.sectionSize(0) / 2) - 7), 6)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._position_header_checkbox()

    def _update_empty_state(self):
        if not self.empty_label or not self.clear_filter_btn or not self.retry_btn or not self.empty_card or not self.table_card:
            return
        has_rows = len(self.filtered_rows) > 0
        has_error = bool(self.load_error)
        if has_error:
            self.empty_label.setText(self.load_error)
            self.clear_filter_btn.hide()
            self.retry_btn.show()
            self.empty_card.show()
            self.table_card.hide()
            return
        if not has_rows:
            self.empty_label.setText("Không tìm thấy tài khoản phù hợp.")
            self.clear_filter_btn.show()
            self.retry_btn.hide()
            self.empty_card.show()
            self.table_card.hide()
            return
        self.empty_card.hide()
        self.table_card.show()

    def refresh(self):
        self.rows = self.load_rows()
        self.filtered_rows = [row for row in self.rows if self.accept_row(row)]
        valid_ids = {row.get("user_id") for row in self.rows}
        self.selected_user_ids = {user_id for user_id in self.selected_user_ids if user_id in valid_ids}
        self._render_stats()
        self._render_table()
        self._position_header_checkbox()

    def view_account(self, item):
        status_text = "Đã xóa mềm" if item.get("deleted_at") else ("Hoạt động" if _is_active(item) else "Bị khóa")
        self._show_info(
            "Chi tiết tài khoản",
            f"Tên: {item.get('full_name') or item.get('username')}\n"
            f"Email: {item.get('email') or 'Chưa có'}\n"
            f"SĐT: {item.get('phone') or 'Chưa có'}\n"
            f"Vai trò: {_role_label(item.get('role'))}\n"
            f"Trạng thái: {status_text}\n"
            f"Ngày tạo: {_format_datetime(item.get('created_at'))}\n"
            f"Lần cập nhật hồ sơ: {_format_datetime(item.get('profile_updated_at'))}",
        )

    def add_account(self):
        fields = [
            {"key": "username", "label": "Tên đăng nhập"},
            {"key": "full_name", "label": "Họ và tên"},
            {"key": "email", "label": "Email"},
            {"key": "phone", "label": "Số điện thoại"},
            {"key": "password", "label": "Mật khẩu", "type": "password"},
            {"key": "confirm_password", "label": "Xác nhận mật khẩu", "type": "password"},
            {"key": "role", "label": "Vai trò", "type": "combo", "options": ACCOUNT_ROLE_OPTIONS},
            {"key": "is_active", "label": "Trạng thái", "type": "combo", "options": [("Hoạt động", 1), ("Bị khóa", 0)]},
        ]
        dialog = FormDialog("Thêm tài khoản", fields, parent=self)
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return
        data = dialog.values()
        if not data.get("username") or not data.get("password"):
            self._show_info("Thiếu dữ liệu", "Vui lòng nhập tên đăng nhập và mật khẩu.")
            return
        if data.get("password") != data.get("confirm_password"):
            self._show_info("Mật khẩu", "Mật khẩu xác nhận không khớp.")
            return
        if len(_as_text(data.get("password"))) < 6:
            self._show_info("Mật khẩu", "Mật khẩu tối thiểu 6 ký tự.")
            return
        if "@" not in _as_text(data.get("email")):
            self._show_info("Email", "Email không đúng định dạng.")
            return
        exists = _safe_fetch_all("SELECT user_id FROM Users WHERE username=?", (data.get("username"),))
        if exists:
            self._show_info("Trùng dữ liệu", "Tên đăng nhập đã tồn tại.")
            return
        ok = _safe_execute(
            "INSERT INTO Users (username, password, role, is_active) VALUES (?, ?, ?, ?)",
            (data["username"], _hash_password(data["password"]), _db_role(data["role"]), data["is_active"]),
        )
        if ok:
            user = _safe_fetch_all("SELECT user_id FROM Users WHERE username=?", (data["username"],))
            user_id = user[0].get("user_id") if user else None
            role = data.get("role")
            if role == "doctor" and user_id:
                _safe_execute(
                    "INSERT INTO Doctors (name, specialty, phone, email, user_id, is_active) VALUES (?, ?, ?, ?, ?, ?)",
                    (data.get("full_name") or data.get("username"), None, data.get("phone"), data.get("email"), user_id, data.get("is_active")),
                )
            elif user_id:
                _safe_execute(
                    "INSERT INTO Patients (name, phone, email, user_id, is_active) VALUES (?, ?, ?, ?, ?)",
                    (data.get("full_name") or data.get("username"), data.get("phone"), data.get("email"), user_id, data.get("is_active")),
                )
        self._show_info("Tài khoản", "Thêm tài khoản thành công" if ok else "Không thể tạo tài khoản.")
        self.refresh()

    def edit_account(self, item):
        fields = [
            {"key": "username", "label": "Tên đăng nhập"},
            {"key": "full_name", "label": "Họ và tên"},
            {"key": "email", "label": "Email"},
            {"key": "phone", "label": "Số điện thoại"},
            {"key": "role", "label": "Vai trò", "type": "combo", "options": ACCOUNT_ROLE_OPTIONS},
            {"key": "is_active", "label": "Trạng thái", "type": "combo", "options": [("Hoạt động", 1), ("Bị khóa", 0)]},
        ]
        data = dict(item)
        data["is_active"] = 1 if _is_active(item) else 0
        dialog = FormDialog("Sửa tài khoản", fields, data, self)
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return
        values = dialog.values()
        if "@" not in _as_text(values.get("email")):
            self._show_info("Email", "Email không đúng định dạng.")
            return
        ok = _safe_execute(
            "UPDATE Users SET username=?, role=?, is_active=? WHERE user_id=?",
            (values["username"], _db_role(values["role"]), values["is_active"], item.get("user_id")),
        )
        if ok and values.get("role") == "doctor":
            _safe_execute(
                "UPDATE Doctors SET name=?, phone=?, email=?, is_active=? WHERE user_id=?",
                (values.get("full_name") or values.get("username"), values.get("phone"), values.get("email"), values.get("is_active"), item.get("user_id")),
            )
        elif ok:
            _safe_execute(
                "UPDATE Patients SET name=?, phone=?, email=?, is_active=? WHERE user_id=?",
                (values.get("full_name") or values.get("username"), values.get("phone"), values.get("email"), values.get("is_active"), item.get("user_id")),
            )
        self._show_info("Tài khoản", "Cập nhật tài khoản thành công" if ok else "Không thể cập nhật tài khoản.")
        self.refresh()

    def toggle_account(self, item):
        if item.get("deleted_at"):
            self._show_info("Trạng thái", "Tài khoản đã xóa mềm, không thể khóa/mở khóa trực tiếp.")
            return
        new_state = 0 if _is_active(item) else 1
        if item.get("role") == "admin" and new_state == 0:
            active_admins = sum(1 for row in self.rows if row.get("role") == "admin" and _is_active(row))
            if active_admins <= 1:
                self._show_info("Bảo vệ Admin", "Không thể khóa admin hoạt động cuối cùng.")
                return
        if new_state == 0:
            reason, ok_reason = QtWidgets.QInputDialog.getText(self, "Khóa tài khoản", "Nhập lý do khóa:")
            if not ok_reason:
                return
            if not _as_text(reason).strip():
                self._show_info("Khóa tài khoản", "Cần nhập lý do khóa.")
                return
        if not self._confirm("Cập nhật trạng thái", "Bạn có chắc muốn cập nhật trạng thái tài khoản này?"):
            return
        ok = _safe_execute("UPDATE Users SET is_active=? WHERE user_id=?", (new_state, item.get("user_id")))
        self._show_info("Tài khoản", "Khóa/Mở khóa tài khoản thành công" if ok else "Không thể cập nhật trạng thái.")
        self.refresh()

    def soft_delete_account(self, item):
        if item.get("user_id") == self.user_data.get("user_id"):
            self._show_info("Xóa tài khoản", "Không thể xóa chính tài khoản đang đăng nhập.")
            return
        if item.get("role") == "admin":
            active_admins = sum(1 for row in self.rows if row.get("role") == "admin" and not row.get("deleted_at"))
            if active_admins <= 1:
                self._show_info("Xóa tài khoản", "Không thể xóa quản trị viên cuối cùng.")
                return
        if not self._confirm("Xóa tài khoản", "Bạn có chắc chắn muốn xóa tài khoản này không?"):
            return
        ok = _safe_execute(
            "UPDATE Users SET is_active=0, deleted_at=? WHERE user_id=?",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), item.get("user_id")),
        )
        self._show_info("Xóa tài khoản", "Xóa tài khoản thành công" if ok else "Không thể xóa tài khoản.")
        self.refresh()

    def reset_password(self, item):
        if not self._confirm("Reset mật khẩu", f"Reset mật khẩu tài khoản {item.get('username')} về 123456?"):
            return
        ok = _safe_execute("UPDATE Users SET password=? WHERE user_id=?", (_hash_password("123456"), item.get("user_id")))
        self._show_info("Reset mật khẩu", "Mật khẩu mới là 123456." if ok else "Không thể reset mật khẩu.")

    def _selected_rows(self):
        selected = [row for row in self.rows if row.get("user_id") in self.selected_user_ids]
        return selected

    def _apply_bulk_status(self, new_state):
        selected = self._selected_rows()
        if not selected:
            self._show_info("Thao tác hàng loạt", "Vui lòng chọn ít nhất 1 tài khoản.")
            return
        if new_state == 0:
            active_admins = sum(1 for row in self.rows if row.get("role") == "admin" and _is_active(row) and not row.get("deleted_at"))
            selected_active_admins = sum(1 for row in selected if row.get("role") == "admin" and _is_active(row) and not row.get("deleted_at"))
            if active_admins - selected_active_admins <= 0:
                self._show_info("Bảo vệ Admin", "Không thể khóa tất cả quản trị viên hoạt động.")
                return
        if not self._confirm("Thao tác hàng loạt", "Xác nhận cập nhật trạng thái cho các tài khoản đã chọn?"):
            return
        for row in selected:
            _safe_execute("UPDATE Users SET is_active=? WHERE user_id=?", (new_state, row.get("user_id")))
        self._show_info("Thao tác hàng loạt", "Đã cập nhật trạng thái các tài khoản đã chọn.")
        self.refresh()

    def _bulk_soft_delete(self):
        selected = self._selected_rows()
        if not selected:
            self._show_info("Thao tác hàng loạt", "Vui lòng chọn ít nhất 1 tài khoản.")
            return
        current_user_id = self.user_data.get("user_id")
        selected = [row for row in selected if row.get("user_id") != current_user_id]
        if not selected:
            self._show_info("Thao tác hàng loạt", "Không thể xóa tài khoản đang đăng nhập.")
            return
        if not self._confirm("Xóa hàng loạt", "Bạn có chắc chắn muốn xóa mềm các tài khoản đã chọn?"):
            return
        for row in selected:
            _safe_execute(
                "UPDATE Users SET is_active=0, deleted_at=? WHERE user_id=?",
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), row.get("user_id")),
            )
        self._show_info("Xóa hàng loạt", "Đã xóa mềm các tài khoản đã chọn.")
        self.refresh()

    def _bulk_assign_role(self):
        selected = self._selected_rows()
        if not selected:
            self._show_info("Gán vai trò", "Vui lòng chọn ít nhất 1 tài khoản.")
            return
        labels = [label for label, _ in ACCOUNT_ROLE_OPTIONS]
        role_label, ok = QtWidgets.QInputDialog.getItem(self, "Gán vai trò", "Chọn vai trò mới:", labels, editable=False)
        if not ok:
            return
        role_map = {label: value for label, value in ACCOUNT_ROLE_OPTIONS}
        role = _db_role(role_map.get(role_label))
        for row in selected:
            _safe_execute("UPDATE Users SET role=? WHERE user_id=?", (role, row.get("user_id")))
        self._show_info("Gán vai trò", "Đã cập nhật vai trò cho các tài khoản đã chọn.")
        self.refresh()

    def export_excel(self):
        self._export_rows_to_excel(self.filtered_rows)

    def _export_selected_excel(self):
        rows = self._selected_rows()
        if not rows:
            self._show_info("Xuất Excel", "Vui lòng chọn tài khoản để xuất.")
            return
        self._export_rows_to_excel(rows)

    def _export_rows_to_excel(self, rows):
        default_name = f"danh-sach-tai-khoan-{datetime.now().strftime('%d-%m-%Y')}.xlsx"
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Xuất Excel", default_name, "Excel Files (*.xlsx)")
        if not path:
            return
        if not path.lower().endswith(".xlsx"):
            path += ".xlsx"

        # Build a minimal valid XLSX package without third-party dependency.
        import zipfile
        import xml.sax.saxutils as saxutils

        headers = ["STT", "Họ tên", "Email", "SĐT", "Vai trò", "Trạng thái", "Ngày tạo"]
        table_rows = []
        for idx, row in enumerate(rows, 1):
            status = "Đã xóa mềm" if row.get("deleted_at") else ("Hoạt động" if _is_active(row) else "Bị khóa")
            table_rows.append([
                str(idx),
                _as_text(row.get("full_name") or row.get("username")),
                _as_text(row.get("email")),
                _as_text(row.get("phone")),
                _role_label(row.get("role")),
                status,
                _format_datetime(row.get("created_at")),
            ])

        def make_row_xml(index, values):
            cells = []
            for col_idx, value in enumerate(values):
                col = chr(ord('A') + col_idx)
                escaped = saxutils.escape(_as_text(value))
                cells.append(f'<c r="{col}{index}" t="inlineStr"><is><t>{escaped}</t></is></c>')
            return f"<row r=\"{index}\">{''.join(cells)}</row>"

        rows_xml = [make_row_xml(1, headers)]
        for i, values in enumerate(table_rows, 2):
            rows_xml.append(make_row_xml(i, values))
        sheet_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<sheetData>' + ''.join(rows_xml) + '</sheetData>'
            '</worksheet>'
        )

        workbook_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<sheets><sheet name="Accounts" sheetId="1" r:id="rId1"/></sheets>'
            '</workbook>'
        )

        content_types_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '</Types>'
        )

        root_rels_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '</Relationships>'
        )

        workbook_rels_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
            '</Relationships>'
        )

        tmp_fd, tmp_path = tempfile.mkstemp(suffix=".xlsx")
        os.close(tmp_fd)
        try:
            Path(tmp_path).unlink(missing_ok=True)
            with zipfile.ZipFile(tmp_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("[Content_Types].xml", content_types_xml)
                zf.writestr("_rels/.rels", root_rels_xml)
                zf.writestr("xl/workbook.xml", workbook_xml)
                zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml)
                zf.writestr("xl/worksheets/sheet1.xml", sheet_xml)
            shutil.copy2(tmp_path, path)
            self._show_info("Xuất Excel", "Đã xuất Excel theo bộ lọc hiện tại.")
        finally:
            try:
                Path(tmp_path).unlink(missing_ok=True)
            except Exception:
                pass

    def export_row(self, row):
        status = "Đã xóa mềm" if row.get("deleted_at") else ("Hoạt động" if _is_active(row) else "Bị khóa")
        return [
            row.get("user_id"),
            row.get("full_name") or row.get("username"),
            row.get("email"),
            row.get("phone"),
            _role_label(row.get("role")),
            status,
            row.get("created_at"),
        ]


class DoctorManagementPage(AdminListPage):
    page_title = "Quản lý bác sĩ"
    breadcrumb = "Dashboard / Quản lý bác sĩ"
    headers = ["☐", "STT", "Họ và tên", "Chuyên khoa", "SĐT", "Email", "Trạng thái", "Tình trạng", "Ngày tạo", "Thao tác"]
    column_widths = [0.35, 0.45, 1.55, 1.35, 1.05, 1.8, 1.1, 1.15, 1.05, 0.95]
    search_placeholder = "Tìm kiếm bác sĩ (Tên, chuyên khoa, SĐT...)"

    WORK_STATUS_OPTIONS = [
        ("Đang làm việc", "Đang làm việc"),
        ("Nghỉ phép", "Nghỉ phép"),
        ("Tạm nghỉ", "Tạm nghỉ"),
        ("Đã nghỉ việc", "Đã nghỉ việc"),
    ]

    def __init__(self, user_data=None, parent=None):
        self.selected_doctor_ids = set()
        self._header_checkbox = None
        self._suspend_checkbox_sync = False
        self._current_page_rows = []
        self.load_error = ""
        self.empty_card = None
        self.empty_label = None
        self.clear_filter_btn = None
        self.retry_btn = None
        self.table_card = None
        self._search_debounce_timer = None
        super().__init__(user_data, parent)

    def _add_filters(self, layout):
        self.specialty_filter = self._combo([("Tất cả chuyên khoa", "all")])
        self.status_filter = self._combo([
            ("Tất cả trạng thái", "all"),
            ("Hoạt động", "active"),
            ("Tạm nghỉ", "paused"),
            ("Nghỉ việc", "resigned"),
        ])
        self.work_status_filter = self._combo([("Tất cả tình trạng", "all")] + self.WORK_STATUS_OPTIONS)
        layout.addWidget(self.specialty_filter)
        layout.addWidget(self.status_filter)
        layout.addWidget(self.work_status_filter)

    def _add_toolbar_buttons(self, layout):
        add_btn = self._button("Thêm bác sĩ", primary=True)
        add_btn.setFixedWidth(118)
        add_btn.clicked.connect(self.add_doctor)
        layout.addWidget(add_btn)
        export_btn = self._button("Xuất Excel")
        export_btn.setFixedWidth(106)
        export_btn.clicked.connect(self.export_excel)
        layout.addWidget(export_btn)

    def _build_list_page(self):
        super()._build_list_page()
        self.search_input.textChanged.disconnect()
        self._search_debounce_timer = QtCore.QTimer(self)
        self._search_debounce_timer.setSingleShot(True)
        self._search_debounce_timer.timeout.connect(self._reset_and_refresh)
        self.search_input.textChanged.connect(self._on_search_text_changed)
        self.table_card = self.table.parentWidget().parentWidget()

        self.bulk_row = QtWidgets.QHBoxLayout()
        self.bulk_row.setSpacing(8)
        self.bulk_label = QtWidgets.QLabel("Chưa chọn bác sĩ")
        self.bulk_label.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 800;")
        self.bulk_row.addWidget(self.bulk_label)
        self.bulk_row.addStretch()

        self.bulk_active_btn = self._button("Chuyển hoạt động", primary=True)
        self.bulk_pause_btn = self._button("Chuyển tạm nghỉ")
        self.bulk_resign_btn = self._button("Chuyển nghỉ việc", danger=True)
        self.bulk_export_btn = self._button("Xuất đã chọn")
        for btn in [self.bulk_active_btn, self.bulk_pause_btn, self.bulk_resign_btn, self.bulk_export_btn]:
            btn.setVisible(False)
            self.bulk_row.addWidget(btn)

        self.bulk_active_btn.clicked.connect(lambda: self._apply_bulk_status("active"))
        self.bulk_pause_btn.clicked.connect(lambda: self._apply_bulk_status("paused"))
        self.bulk_resign_btn.clicked.connect(lambda: self._apply_bulk_status("resigned"))
        self.bulk_export_btn.clicked.connect(self._export_selected_excel)
        self.table_card.layout().insertLayout(1, self.bulk_row)

        self.empty_card = self._card()
        empty_layout = QtWidgets.QVBoxLayout(self.empty_card)
        empty_layout.setContentsMargins(24, 24, 24, 24)
        empty_layout.setSpacing(10)
        empty_icon = QtWidgets.QLabel("🩺")
        empty_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        empty_icon.setStyleSheet("font-size: 34px;")
        self.empty_label = QtWidgets.QLabel("Không tìm thấy bác sĩ phù hợp.")
        self.empty_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet("font-size: 14px; font-weight: 800; color: #475569;")
        action_row = QtWidgets.QHBoxLayout()
        action_row.addStretch()
        self.clear_filter_btn = self._button("Xóa bộ lọc")
        self.clear_filter_btn.clicked.connect(self._clear_filters)
        self.retry_btn = self._button("Thử lại", primary=True)
        self.retry_btn.clicked.connect(self.refresh)
        action_row.addWidget(self.clear_filter_btn)
        action_row.addWidget(self.retry_btn)
        action_row.addStretch()
        empty_layout.addWidget(empty_icon)
        empty_layout.addWidget(self.empty_label)
        empty_layout.addLayout(action_row)
        self.content_layout.insertWidget(2, self.empty_card)
        self.empty_card.hide()

    def _on_search_text_changed(self):
        if self._search_debounce_timer is not None:
            self._search_debounce_timer.start(350)

    def _clear_filters(self):
        self.search_input.clear()
        self.specialty_filter.setCurrentIndex(0)
        self.status_filter.setCurrentIndex(0)
        self.work_status_filter.setCurrentIndex(0)
        self._reset_and_refresh()

    def _set_loading(self, loading):
        self.search_input.setEnabled(not loading)
        self.specialty_filter.setEnabled(not loading)
        self.status_filter.setEnabled(not loading)
        self.work_status_filter.setEnabled(not loading)
        self.page_size_combo.setEnabled(not loading)
        if loading:
            self.table.setRowCount(4)
            for row in range(4):
                for col in range(self.table.columnCount()):
                    self.table.setItem(row, col, QtWidgets.QTableWidgetItem("Đang tải..."))

    def _sync_bulk_ui(self):
        selected_count = len(self.selected_doctor_ids)
        has_selected = selected_count > 0
        self.bulk_label.setText(f"Đã chọn {selected_count} bác sĩ" if has_selected else "Chưa chọn bác sĩ")
        for btn in [self.bulk_active_btn, self.bulk_pause_btn, self.bulk_resign_btn, self.bulk_export_btn]:
            btn.setVisible(has_selected)

    def _ensure_schema(self):
        # Keep schema migration out of runtime view logic.
        # Database schema should be managed via init_db.sql / migrate scripts.
        return

    @staticmethod
    def _normalize_work_status(row):
        raw = _as_text(row.get("work_status")).strip()
        mapping = {
            "WORKING": "Đang làm việc",
            "ON_LEAVE": "Nghỉ phép",
            "LEFT": "Đã nghỉ việc",
            "ACTIVE": "Đang làm việc",
            "TEMPORARILY_INACTIVE": "Tạm nghỉ",
            "RESIGNED": "Đã nghỉ việc",
            "ĐANG LÀM VIỆC": "Đang làm việc",
            "NGHỈ PHÉP": "Nghỉ phép",
            "TẠM NGHỈ": "Tạm nghỉ",
            "ĐÃ NGHỈ VIỆC": "Đã nghỉ việc",
        }
        if not raw:
            value = "Đang làm việc" if _is_active(row) else "Đã nghỉ việc"
        else:
            value = mapping.get(raw.upper(), raw)
        if not _is_active(row) and value in {"Đang làm việc", "Nghỉ phép", "Tạm nghỉ"}:
            value = "Đã nghỉ việc"
        return value

    def _status_label(self, row):
        work_status = self._normalize_work_status(row)
        if not _is_active(row) or work_status == "Đã nghỉ việc":
            return "Nghỉ việc"
        if work_status in {"Nghỉ phép", "Tạm nghỉ"}:
            return "Tạm nghỉ"
        return "Hoạt động"

    def load_rows(self):
        self._set_loading(True)
        self.load_error = ""
        try:
            rows = _safe_fetch_all(
                """
                SELECT doctor_id, name, specialty, phone, email, is_active, work_status, created_at, updated_at
                FROM Doctors
                ORDER BY doctor_id DESC
                """
            )
            for row in rows:
                row["work_status"] = self._normalize_work_status(row)
            current = self.specialty_filter.currentData()
            self.specialty_filter.blockSignals(True)
            self.specialty_filter.clear()
            self.specialty_filter.addItem("Tất cả chuyên khoa", "all")
            for specialty in sorted({_as_text(row.get("specialty")) for row in rows if row.get("specialty")}):
                self.specialty_filter.addItem(specialty, specialty)
            index = self.specialty_filter.findData(current)
            self.specialty_filter.setCurrentIndex(max(index, 0))
            self.specialty_filter.blockSignals(False)
            return rows
        except Exception as exc:
            self.load_error = f"Không thể tải danh sách bác sĩ. {exc}"
            return []
        finally:
            self._set_loading(False)

    def accept_row(self, row):
        specialty_ok = self.specialty_filter.currentData() == "all" or row.get("specialty") == self.specialty_filter.currentData()
        status_value = self.status_filter.currentData()
        status_label = self._status_label(row)
        status_ok = (
            status_value == "all"
            or (status_value == "active" and status_label == "Hoạt động")
            or (status_value == "paused" and status_label == "Tạm nghỉ")
            or (status_value == "resigned" and status_label == "Nghỉ việc")
        )
        work_choice = self.work_status_filter.currentData()
        work_status = self._normalize_work_status(row)
        work_ok = work_choice == "all" or work_choice == work_status
        search_ok = _contains(row, ["name", "specialty", "phone", "email"], self.search_input.text())
        if not search_ok:
            query = _as_text(self.search_input.text()).strip().lower()
            search_ok = bool(query) and (query in status_label.lower() or query in work_status.lower())
        return specialty_ok and status_ok and work_ok and search_ok

    def stat_cards(self):
        active = sum(1 for row in self.rows if self._status_label(row) == "Hoạt động")
        paused = sum(1 for row in self.rows if self._status_label(row) == "Tạm nghỉ")
        resigned = sum(1 for row in self.rows if self._status_label(row) == "Nghỉ việc")
        return [
            self._stat_card("🩺", "Tổng bác sĩ", len(self.rows), "Dữ liệu theo DB hiện tại", "#2563eb"),
            self._stat_card("👤", "Đang hoạt động", active, "Dữ liệu theo DB hiện tại", "#00a651"),
            self._stat_card("⏸", "Tạm nghỉ", paused, "Dữ liệu theo DB hiện tại", "#f97316"),
            self._stat_card("🚫", "Nghỉ việc", resigned, "Dữ liệu theo DB hiện tại", "#8b5cf6"),
        ]

    def render_row(self, row, data):
        checkbox = QtWidgets.QCheckBox()
        checkbox.setChecked(data.get("doctor_id") in self.selected_doctor_ids)
        checkbox.stateChanged.connect(lambda state, doctor_id=data.get("doctor_id"): self._toggle_selected(doctor_id, state))
        check_wrap = QtWidgets.QWidget()
        check_layout = QtWidgets.QHBoxLayout(check_wrap)
        check_layout.setContentsMargins(0, 0, 0, 0)
        check_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        check_layout.addWidget(checkbox)
        self.table.setCellWidget(row, 0, check_wrap)

        stt = (self.current_page - 1) * self.page_size + row + 1
        self._set_item(row, 1, stt)
        self._set_item(row, 2, f"👨‍⚕️ {_as_text(data.get('name'))}")
        self._set_item(row, 3, data.get("specialty"))
        self._set_item(row, 4, data.get("phone"))
        self._set_item(row, 5, data.get("email"))

        status_text = self._status_label(data)
        status_kind = "success" if status_text == "Hoạt động" else ("warning" if status_text == "Tạm nghỉ" else "danger")
        self.table.setCellWidget(row, 6, self._badge(status_text, status_kind))

        work_status = self._normalize_work_status(data)
        work_kind = "success" if work_status == "Đang làm việc" else ("warning" if work_status in {"Nghỉ phép", "Tạm nghỉ"} else "danger")
        self.table.setCellWidget(row, 7, self._badge(work_status, work_kind))

        self._set_item(row, 8, _format_date(data.get("created_at")))
        view_btn = self._icon_button("Xem", "info")
        edit_btn = self._icon_button("Sửa", "info")
        del_btn = self._icon_button("Xóa", "danger")
        view_btn.clicked.connect(lambda _, item=data: self.view_detail(item))
        edit_btn.clicked.connect(lambda _, item=data: self.edit_doctor(item))
        del_btn.clicked.connect(lambda _, item=data: self.soft_delete(item))
        self.table.setCellWidget(row, 9, self._action_cell([view_btn, edit_btn, del_btn]))

    def _toggle_selected(self, doctor_id, state):
        if self._suspend_checkbox_sync or not doctor_id:
            return
        if state == int(QtCore.Qt.CheckState.Checked):
            self.selected_doctor_ids.add(doctor_id)
        else:
            self.selected_doctor_ids.discard(doctor_id)
        self._sync_bulk_ui()
        self._sync_header_checkbox()

    def _sync_header_checkbox(self):
        if not self._header_checkbox:
            return
        page_ids = [row.get("doctor_id") for row in self._current_page_rows if row.get("doctor_id")]
        if not page_ids:
            self._header_checkbox.setCheckState(QtCore.Qt.CheckState.Unchecked)
            return
        selected_in_page = sum(1 for doctor_id in page_ids if doctor_id in self.selected_doctor_ids)
        self._header_checkbox.blockSignals(True)
        if selected_in_page == 0:
            self._header_checkbox.setCheckState(QtCore.Qt.CheckState.Unchecked)
        elif selected_in_page == len(page_ids):
            self._header_checkbox.setCheckState(QtCore.Qt.CheckState.Checked)
        else:
            self._header_checkbox.setCheckState(QtCore.Qt.CheckState.PartiallyChecked)
        self._header_checkbox.blockSignals(False)

    def _toggle_select_page(self, state):
        page_ids = [row.get("doctor_id") for row in self._current_page_rows if row.get("doctor_id")]
        if state == int(QtCore.Qt.CheckState.Checked):
            for doctor_id in page_ids:
                self.selected_doctor_ids.add(doctor_id)
        elif state == int(QtCore.Qt.CheckState.Unchecked):
            for doctor_id in page_ids:
                self.selected_doctor_ids.discard(doctor_id)
        self._render_table()
        self._sync_bulk_ui()

    def _setup_header_checkbox(self):
        header = self.table.horizontalHeader()
        if self._header_checkbox is not None:
            self._header_checkbox.deleteLater()
            self._header_checkbox = None
        box = QtWidgets.QCheckBox(header)
        box.setTristate(True)
        box.stateChanged.connect(self._toggle_select_page)
        box.show()
        self._header_checkbox = box
        self._position_header_checkbox()

    def _position_header_checkbox(self):
        if not self._header_checkbox:
            return
        header = self.table.horizontalHeader()
        geo = header.sectionPosition(0)
        self._header_checkbox.move(geo + max(0, int(header.sectionSize(0) / 2) - 7), 6)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._position_header_checkbox()

    def _update_empty_state(self):
        if not self.empty_label or not self.clear_filter_btn or not self.retry_btn or not self.empty_card or not self.table_card:
            return
        has_rows = len(self.filtered_rows) > 0
        has_error = bool(self.load_error)
        if has_error:
            self.empty_label.setText(self.load_error)
            self.clear_filter_btn.hide()
            self.retry_btn.show()
            self.empty_card.show()
            self.table_card.hide()
            return
        if not has_rows:
            self.empty_label.setText("Không tìm thấy bác sĩ phù hợp.")
            self.clear_filter_btn.show()
            self.retry_btn.hide()
            self.empty_card.show()
            self.table_card.hide()
            return
        self.empty_card.hide()
        self.table_card.show()

    def _render_table(self):
        total_pages = max(1, (len(self.filtered_rows) + self.page_size - 1) // self.page_size)
        self.current_page = min(max(1, self.current_page), total_pages)
        start = (self.current_page - 1) * self.page_size
        visible = self.filtered_rows[start:start + self.page_size]
        self._current_page_rows = visible
        self.table.setRowCount(len(visible))
        for row_index, row_data in enumerate(visible):
            self.render_row(row_index, row_data)
        self.total_label.setText(f"{len(self.filtered_rows)} bản ghi")
        self.page_label.setText(f"Trang {self.current_page}/{total_pages}")
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)
        self.table.resizeRowsToContents()
        for row in range(self.table.rowCount()):
            self.table.setRowHeight(row, max(self.table.rowHeight(row), 44))
        self._apply_column_widths()
        target_rows = max(len(visible), min(self.page_size, 10))
        self.table.setFixedHeight(42 + target_rows * 44 + 4)
        self._setup_header_checkbox()
        self._sync_header_checkbox()
        self._sync_bulk_ui()
        self._update_empty_state()

    def refresh(self):
        self.rows = self.load_rows()
        self.filtered_rows = [row for row in self.rows if self.accept_row(row)]
        valid_ids = {row.get("doctor_id") for row in self.rows}
        self.selected_doctor_ids = {doctor_id for doctor_id in self.selected_doctor_ids if doctor_id in valid_ids}
        self._render_stats()
        self._render_table()
        self._position_header_checkbox()

    @staticmethod
    def _email_valid(email):
        text = _as_text(email).strip()
        return not text or ("@" in text and not text.startswith("@") and not text.endswith("@"))

    @staticmethod
    def _phone_valid(phone):
        digits = "".join(ch for ch in _as_text(phone) if ch.isdigit())
        return 9 <= len(digits) <= 11

    def _doctor_fields(self):
        return [
            {"key": "name", "label": "Họ và tên"},
            {"key": "specialty", "label": "Chuyên khoa"},
            {"key": "phone", "label": "SĐT"},
            {"key": "email", "label": "Email"},
            {
                "key": "is_active",
                "label": "Trạng thái",
                "type": "combo",
                "options": [("Hoạt động", 1), ("Nghỉ việc", 0)],
            },
            {
                "key": "work_status",
                "label": "Tình trạng",
                "type": "combo",
                "options": self.WORK_STATUS_OPTIONS,
            },
        ]

    def _validate_doctor_payload(self, data, current_id=None):
        if not _as_text(data.get("name")).strip():
            return "Họ và tên không được để trống."
        if not _as_text(data.get("specialty")).strip():
            return "Vui lòng chọn hoặc nhập chuyên khoa."
        if not self._phone_valid(data.get("phone")):
            return "Số điện thoại phải có từ 9 đến 11 chữ số."
        if not self._email_valid(data.get("email")):
            return "Email không đúng định dạng."

        if _as_text(data.get("email")).strip():
            rows = _safe_fetch_all("SELECT doctor_id FROM Doctors WHERE email=?", (data.get("email"),))
            for row in rows:
                if current_id is None or str(row.get("doctor_id")) != str(current_id):
                    return "Email đã tồn tại."
        rows = _safe_fetch_all("SELECT doctor_id FROM Doctors WHERE phone=?", (data.get("phone"),))
        for row in rows:
            if current_id is None or str(row.get("doctor_id")) != str(current_id):
                return "Số điện thoại đã tồn tại."
        return ""

    def add_doctor(self):
        dialog = FormDialog("Thêm bác sĩ", self._doctor_fields(), {"is_active": 1, "work_status": "Đang làm việc"}, self)
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return
        data = dialog.values()
        if int(data.get("is_active") or 0) == 0:
            data["work_status"] = "Đã nghỉ việc"
        error = self._validate_doctor_payload(data)
        if error:
            self._show_info("Thiếu dữ liệu", error)
            return
        ok = _safe_execute(
            """
            INSERT INTO Doctors (name, specialty, phone, email, is_active, work_status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """,
            (data["name"], data["specialty"], data["phone"], data["email"], data["is_active"], data["work_status"]),
        )
        if not ok:
            ok = _safe_execute(
                "INSERT INTO Doctors (name, specialty, phone, email, is_active) VALUES (?, ?, ?, ?, ?)",
                (data["name"], data["specialty"], data["phone"], data["email"], data["is_active"]),
            )
        self._show_info("Bác sĩ", "Thêm bác sĩ thành công." if ok else "Không thể thêm bác sĩ.")
        self.refresh()

    def edit_doctor(self, item):
        data = dict(item)
        data["is_active"] = 1 if _is_active(item) else 0
        data["work_status"] = self._normalize_work_status(item)
        dialog = FormDialog("Sửa bác sĩ", self._doctor_fields(), data, self)
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return
        values = dialog.values()
        if int(values.get("is_active") or 0) == 0:
            values["work_status"] = "Đã nghỉ việc"
        error = self._validate_doctor_payload(values, item.get("doctor_id"))
        if error:
            self._show_info("Thiếu dữ liệu", error)
            return
        ok = _safe_execute(
            """
            UPDATE Doctors
            SET name=?, specialty=?, phone=?, email=?, is_active=?, work_status=?, updated_at=CURRENT_TIMESTAMP
            WHERE doctor_id=?
            """,
            (
                values["name"],
                values["specialty"],
                values["phone"],
                values["email"],
                values["is_active"],
                values["work_status"],
                item.get("doctor_id"),
            ),
        )
        if not ok:
            ok = _safe_execute(
                "UPDATE Doctors SET name=?, specialty=?, phone=?, email=?, is_active=? WHERE doctor_id=?",
                (
                    values["name"],
                    values["specialty"],
                    values["phone"],
                    values["email"],
                    values["is_active"],
                    item.get("doctor_id"),
                ),
            )
        self._show_info("Bác sĩ", "Đã cập nhật bác sĩ." if ok else "Không thể cập nhật bác sĩ.")
        self.refresh()

    def view_detail(self, item):
        self._show_info(
            "Chi tiết bác sĩ",
            f"Mã bác sĩ: {item.get('doctor_id')}\n"
            f"Họ và tên: {item.get('name')}\n"
            f"Chuyên khoa: {item.get('specialty') or 'Chưa cập nhật'}\n"
            f"SĐT: {item.get('phone') or 'Chưa cập nhật'}\n"
            f"Email: {item.get('email') or 'Chưa cập nhật'}\n"
            f"Trạng thái: {self._status_label(item)}\n"
            f"Tình trạng: {self._normalize_work_status(item)}\n"
            f"Ngày tạo: {_format_date(item.get('created_at'))}\n"
            f"Cập nhật gần nhất: {_format_datetime(item.get('updated_at'))}",
        )

    def soft_delete(self, item):
        if not self._confirm("Xóa bác sĩ", "Bác sĩ sẽ được chuyển sang trạng thái nghỉ việc. Tiếp tục?"):
            return
        related = _safe_fetch_all(
            "SELECT COUNT(*) AS total FROM Appointments WHERE doctor_id=?",
            (item.get("doctor_id"),),
        )
        related_count = _as_int((related[0] if related else {}).get("total"))
        ok = _safe_execute(
            "UPDATE Doctors SET is_active=0, work_status='Đã nghỉ việc', updated_at=CURRENT_TIMESTAMP WHERE doctor_id=?",
            (item.get("doctor_id"),),
        )
        if ok and related_count > 0:
            self._show_info(
                "Bác sĩ",
                "Bác sĩ đã có dữ liệu lịch khám nên hệ thống áp dụng ngừng hoạt động (soft delete) thay vì xóa cứng.",
            )
        else:
            self._show_info("Bác sĩ", "Đã ngừng hoạt động bác sĩ." if ok else "Không thể cập nhật trạng thái.")
        self.refresh()

    def _selected_rows(self):
        return [row for row in self.rows if row.get("doctor_id") in self.selected_doctor_ids]

    def _apply_bulk_status(self, mode):
        selected = self._selected_rows()
        if not selected:
            self._show_info("Thao tác hàng loạt", "Vui lòng chọn ít nhất 1 bác sĩ.")
            return
        if not self._confirm("Thao tác hàng loạt", "Xác nhận cập nhật trạng thái cho các bác sĩ đã chọn?"):
            return
        success_count = 0
        for row in selected:
            doctor_id = row.get("doctor_id")
            if mode == "active":
                ok = _safe_execute(
                    "UPDATE Doctors SET is_active=1, work_status='Đang làm việc', updated_at=CURRENT_TIMESTAMP WHERE doctor_id=?",
                    (doctor_id,),
                )
            elif mode == "paused":
                ok = _safe_execute(
                    "UPDATE Doctors SET is_active=1, work_status='Tạm nghỉ', updated_at=CURRENT_TIMESTAMP WHERE doctor_id=?",
                    (doctor_id,),
                )
            else:
                ok = _safe_execute(
                    "UPDATE Doctors SET is_active=0, work_status='Đã nghỉ việc', updated_at=CURRENT_TIMESTAMP WHERE doctor_id=?",
                    (doctor_id,),
                )
            if ok:
                success_count += 1
        if success_count == len(selected):
            self._show_info("Thao tác hàng loạt", "Đã cập nhật trạng thái các bác sĩ đã chọn.")
        elif success_count == 0:
            self._show_info("Thao tác hàng loạt", "Không thể cập nhật trạng thái bác sĩ nào.")
        else:
            self._show_info(
                "Thao tác hàng loạt",
                f"Đã cập nhật {success_count}/{len(selected)} bác sĩ. Vui lòng kiểm tra lại các bản ghi còn lại.",
            )
        self.refresh()

    def export_excel(self):
        options = [
            "Xuất theo bộ lọc hiện tại",
            "Xuất toàn bộ danh sách",
            "Xuất các dòng đã chọn",
        ]
        choice, ok = QtWidgets.QInputDialog.getItem(self, "Xuất Excel", "Chọn phạm vi xuất:", options, editable=False)
        if not ok:
            return
        if choice == options[0]:
            rows = self.filtered_rows
        elif choice == options[1]:
            rows = self.rows
        else:
            rows = self._selected_rows()
        if not rows:
            self._show_info("Xuất Excel", "Không có dữ liệu để xuất theo lựa chọn hiện tại.")
            return
        self._export_rows_to_excel(rows)

    def _export_selected_excel(self):
        rows = self._selected_rows()
        if not rows:
            self._show_info("Xuất Excel", "Vui lòng chọn bác sĩ để xuất.")
            return
        self._export_rows_to_excel(rows)

    def _export_rows_to_excel(self, rows):
        default_name = f"danh_sach_bac_si_{datetime.now().strftime('%Y_%m_%d')}.xlsx"
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Xuất Excel", default_name, "Excel Files (*.xlsx)")
        if not path:
            return
        if not path.lower().endswith(".xlsx"):
            path += ".xlsx"

        import zipfile
        import xml.sax.saxutils as saxutils

        headers = ["STT", "Họ và tên", "Chuyên khoa", "SĐT", "Email", "Trạng thái", "Tình trạng", "Ngày tạo", "Ngày cập nhật"]
        table_rows = []
        for idx, row in enumerate(rows, 1):
            table_rows.append([
                str(idx),
                _as_text(row.get("name")),
                _as_text(row.get("specialty")),
                _as_text(row.get("phone")),
                _as_text(row.get("email")),
                self._status_label(row),
                self._normalize_work_status(row),
                _format_date(row.get("created_at")),
                _format_datetime(row.get("updated_at")),
            ])

        def make_row_xml(index, values):
            cells = []
            for col_idx, value in enumerate(values):
                col = chr(ord("A") + col_idx)
                escaped = saxutils.escape(_as_text(value))
                cells.append(f'<c r="{col}{index}" t="inlineStr"><is><t>{escaped}</t></is></c>')
            return f"<row r=\"{index}\">{''.join(cells)}</row>"

        rows_xml = [make_row_xml(1, headers)]
        for i, values in enumerate(table_rows, 2):
            rows_xml.append(make_row_xml(i, values))
        sheet_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<sheetData>' + "".join(rows_xml) + "</sheetData>"
            "</worksheet>"
        )

        workbook_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<sheets><sheet name="Doctors" sheetId="1" r:id="rId1"/></sheets>'
            "</workbook>"
        )

        content_types_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            "</Types>"
        )

        root_rels_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            "</Relationships>"
        )

        workbook_rels_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
            "</Relationships>"
        )

        tmp_fd, tmp_path = tempfile.mkstemp(suffix=".xlsx")
        os.close(tmp_fd)
        try:
            Path(tmp_path).unlink(missing_ok=True)
            try:
                with zipfile.ZipFile(tmp_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                    zf.writestr("[Content_Types].xml", content_types_xml)
                    zf.writestr("_rels/.rels", root_rels_xml)
                    zf.writestr("xl/workbook.xml", workbook_xml)
                    zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml)
                    zf.writestr("xl/worksheets/sheet1.xml", sheet_xml)
                shutil.copy2(tmp_path, path)
                self._show_info("Xuất Excel", "Đã xuất Excel theo lựa chọn hiện tại.")
            except Exception as exc:
                self._show_info("Xuất Excel", f"Không thể xuất Excel: {exc}")
        finally:
            try:
                Path(tmp_path).unlink(missing_ok=True)
            except Exception:
                pass

    def export_row(self, row):
        return [
            row.get("doctor_id"),
            row.get("name"),
            row.get("specialty"),
            row.get("phone"),
            row.get("email"),
            self._status_label(row),
            self._normalize_work_status(row),
            _format_date(row.get("created_at")),
            _format_datetime(row.get("updated_at")),
        ]


class PatientManagementPage(AdminListPage):
    page_title = "Quản lý bệnh nhân"
    breadcrumb = "Dashboard / Quản lý bệnh nhân"
    headers = ["☐", "STT", "Họ và tên", "Giới tính", "Ngày sinh", "SĐT", "CCCD/CMND", "Email", "Địa chỉ", "Trạng thái", "Thao tác"]
    column_widths = [0.35, 0.45, 1.45, 0.75, 1.0, 1.05, 1.25, 1.75, 1.0, 1.15, 0.9]
    search_placeholder = "Tìm kiếm bệnh nhân (Tên, SĐT, CCCD, Email...)"

    def _add_filters(self, layout):
        self.gender_filter = self._combo([("Tất cả giới tính", "all"), ("Nam", "Nam"), ("Nữ", "Nữ")])
        self.age_filter = self._combo([("Tất cả nhóm tuổi", "all"), ("< 18", "under18"), ("18-60", "adult"), ("> 60", "senior")])
        self.status_filter = self._combo([("Tất cả trạng thái", "all"), ("Hoạt động", "active"), ("Ngưng hoạt động", "inactive")])
        layout.addWidget(self.gender_filter)
        layout.addWidget(self.age_filter)
        layout.addWidget(self.status_filter)

    def _add_toolbar_buttons(self, layout):
        add_btn = self._button("Thêm bệnh nhân", primary=True)
        add_btn.setFixedWidth(138)
        add_btn.clicked.connect(self.add_patient)
        layout.addWidget(add_btn)
        super()._add_toolbar_buttons(layout)

    def load_rows(self):
        return _safe_fetch_all("SELECT * FROM Patients ORDER BY patient_id DESC")

    def accept_row(self, row):
        gender_ok = self.gender_filter.currentData() == "all" or row.get("gender") == self.gender_filter.currentData()
        age = _age_from_dob(row.get("dob"))
        age_choice = self.age_filter.currentData()
        age_ok = (
            age_choice == "all"
            or (age is not None and age_choice == "under18" and age < 18)
            or (age is not None and age_choice == "adult" and 18 <= age <= 60)
            or (age is not None and age_choice == "senior" and age > 60)
        )
        status = "active" if _is_active(row) else "inactive"
        status_ok = self.status_filter.currentData() == "all" or status == self.status_filter.currentData()
        return gender_ok and age_ok and status_ok and _contains(row, ["name", "phone", "cccd", "email"], self.search_input.text())

    def stat_cards(self):
        active_rows = [row for row in self.rows if _is_active(row)]
        today = date.today()
        month_start = today.replace(day=1)
        new_count = sum(1 for row in self.rows if (_parse_date(row.get("created_at")) or date.min) >= month_start)
        male = sum(1 for row in active_rows if row.get("gender") == "Nam")
        female = sum(1 for row in active_rows if row.get("gender") == "Nữ")
        return [
            self._stat_card("👥", "Tổng bệnh nhân", len(active_rows), "Dữ liệu theo DB hiện tại", "#2563eb"),
            self._stat_card("💚", "Bệnh nhân mới", new_count, "Dữ liệu theo DB hiện tại", "#00a651"),
            self._stat_card("♂", "Bệnh nhân nam", male, "Dữ liệu theo DB hiện tại", "#f97316"),
            self._stat_card("♀", "Bệnh nhân nữ", female, "Dữ liệu theo DB hiện tại", "#8b5cf6"),
        ]

    def render_row(self, row, data):
        self._set_item(row, 0, "☐")
        self._set_item(row, 1, row + 1)
        self._set_item(row, 2, f"👤 {_as_text(data.get('name'))}")
        self._set_item(row, 3, data.get("gender"))
        self._set_item(row, 4, _format_date(data.get("dob")))
        self._set_item(row, 5, data.get("phone"))
        self._set_item(row, 6, data.get("cccd"))
        self._set_item(row, 7, data.get("email"))
        self._set_item(row, 8, data.get("address"))
        self.table.setCellWidget(row, 9, self._badge("Hoạt động" if _is_active(data) else "Ngưng hoạt động"))
        view_btn = self._icon_button("Xem", "info")
        edit_btn = self._icon_button("Sửa", "info")
        del_btn = self._icon_button("Xóa", "danger")
        view_btn.clicked.connect(lambda _, item=data: self.view_detail(item))
        edit_btn.clicked.connect(lambda _, item=data: self.edit_patient(item))
        del_btn.clicked.connect(lambda _, item=data: self.soft_delete(item))
        self.table.setCellWidget(row, 10, self._action_cell([view_btn, edit_btn, del_btn]))

    def _patient_fields(self):
        return [
            {"key": "name", "label": "Họ và tên"},
            {"key": "dob", "label": "Ngày sinh", "type": "date"},
            {"key": "gender", "label": "Giới tính", "type": "combo", "options": [("Nam", "Nam"), ("Nữ", "Nữ")]},
            {"key": "phone", "label": "SĐT"},
            {"key": "cccd", "label": "CCCD/CMND"},
            {"key": "email", "label": "Email"},
            {"key": "address", "label": "Địa chỉ"},
            {"key": "occupation", "label": "Nghề nghiệp"},
            {"key": "is_active", "label": "Trạng thái", "type": "combo", "options": [("Hoạt động", 1), ("Ngưng hoạt động", 0)]},
        ]

    def add_patient(self):
        dialog = FormDialog("Thêm bệnh nhân", self._patient_fields(), {"gender": "Nam", "is_active": 1}, self)
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return
        data = dialog.values()
        ok = _safe_execute(
            """
            INSERT INTO Patients (name, dob, gender, phone, cccd, email, address, occupation, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (data["name"], data["dob"], data["gender"], data["phone"], data["cccd"], data["email"], data["address"], data["occupation"], data["is_active"]),
        )
        self._show_info("Bệnh nhân", "Đã thêm bệnh nhân." if ok else "Không thể thêm bệnh nhân.")
        self.refresh()

    def edit_patient(self, item):
        data = dict(item)
        data["is_active"] = 1 if _is_active(item) else 0
        dialog = FormDialog("Sửa bệnh nhân", self._patient_fields(), data, self)
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return
        values = dialog.values()
        ok = _safe_execute(
            """
            UPDATE Patients
            SET name=?, dob=?, gender=?, phone=?, cccd=?, email=?, address=?, occupation=?, is_active=?
            WHERE patient_id=?
            """,
            (values["name"], values["dob"], values["gender"], values["phone"], values["cccd"], values["email"], values["address"], values["occupation"], values["is_active"], item.get("patient_id")),
        )
        self._show_info("Bệnh nhân", "Đã cập nhật bệnh nhân." if ok else "Không thể cập nhật bệnh nhân.")
        self.refresh()

    def view_detail(self, item):
        self._show_info(
            "Chi tiết bệnh nhân",
            f"{item.get('name')}\nDOB: {_format_date(item.get('dob'))}\nSĐT: {item.get('phone')}\nCCCD: {item.get('cccd') or 'Chưa có'}\nEmail: {item.get('email') or 'Chưa có'}\nĐịa chỉ: {item.get('address') or 'Chưa có'}",
        )

    def soft_delete(self, item):
        if not self._confirm("Xóa bệnh nhân", "Hồ sơ bệnh nhân sẽ được ngưng hoạt động để giữ lịch sử y tế. Tiếp tục?"):
            return
        ok = _safe_execute("UPDATE Patients SET is_active=0 WHERE patient_id=?", (item.get("patient_id"),))
        self._show_info("Bệnh nhân", "Đã ngưng hoạt động bệnh nhân." if ok else "Không thể cập nhật trạng thái.")
        self.refresh()

    def export_row(self, row):
        return [row.get("patient_id"), row.get("name"), row.get("gender"), row.get("dob"), row.get("phone"), row.get("cccd"), row.get("email"), _is_active(row)]


class MedicineManagementPage(AdminListPage):
    page_title = "Quản lý thuốc"
    breadcrumb = "Dashboard / Quản lý thuốc"
    headers = ["☐", "STT", "Tên thuốc", "Hoạt chất", "Danh mục", "Đơn vị", "Nhà cung cấp", "Số lượng", "Giá nhập", "Giá bán", "Trạng thái", "Thao tác"]
    column_widths = [0.32, 0.45, 1.35, 1.05, 1.35, 0.75, 1.25, 0.8, 0.9, 0.9, 1.05, 0.9]
    search_placeholder = "Tìm kiếm thuốc (Tên thuốc, hoạt chất, mã thuốc...)"

    def _add_filters(self, layout):
        self.category_filter = self._combo([("Danh mục: Tất cả", "all")])
        self.supplier_filter = self._combo([("Nhà cung cấp: Tất cả", "all")])
        self.stock_filter = self._combo([("Trạng thái: Tất cả", "all"), ("Còn hàng", "available"), ("Sắp hết", "low"), ("Hết hàng", "empty")])
        layout.addWidget(self.category_filter)
        layout.addWidget(self.supplier_filter)
        layout.addWidget(self.stock_filter)

    def _add_toolbar_buttons(self, layout):
        add_btn = self._button("Thêm thuốc", primary=True)
        add_btn.setFixedWidth(112)
        add_btn.clicked.connect(self.add_medicine)
        layout.addWidget(add_btn)
        super()._add_toolbar_buttons(layout)

    def load_rows(self):
        rows = _safe_fetch_all("SELECT * FROM Medicines ORDER BY medicine_id DESC")
        self._sync_combo(self.category_filter, "Danh mục: Tất cả", {row.get("category") for row in rows if row.get("category")})
        self._sync_combo(self.supplier_filter, "Nhà cung cấp: Tất cả", {row.get("supplier") for row in rows if row.get("supplier")})
        return rows

    def _sync_combo(self, combo, first_label, values):
        current = combo.currentData()
        combo.blockSignals(True)
        combo.clear()
        combo.addItem(first_label, "all")
        for value in sorted(values):
            combo.addItem(_as_text(value), value)
        index = combo.findData(current)
        combo.setCurrentIndex(max(index, 0))
        combo.blockSignals(False)

    def _stock_state(self, row):
        qty = _as_int(row.get("quantity"))
        if qty <= 0:
            return "empty", "Hết hàng"
        if qty <= 350:
            return "low", "Sắp hết"
        return "available", "Còn hàng"

    def accept_row(self, row):
        stock_key, _ = self._stock_state(row)
        category_ok = self.category_filter.currentData() == "all" or row.get("category") == self.category_filter.currentData()
        supplier_ok = self.supplier_filter.currentData() == "all" or row.get("supplier") == self.supplier_filter.currentData()
        stock_ok = self.stock_filter.currentData() == "all" or stock_key == self.stock_filter.currentData()
        return category_ok and supplier_ok and stock_ok and _contains(
            row,
            ["medicine_code", "name", "active_ingredient", "category", "supplier", "description"],
            self.search_input.text(),
        )

    def stat_cards(self):
        available = sum(1 for row in self.rows if self._stock_state(row)[0] == "available" and _is_active(row))
        low = sum(1 for row in self.rows if self._stock_state(row)[0] == "low" and _is_active(row))
        empty = sum(1 for row in self.rows if self._stock_state(row)[0] == "empty" and _is_active(row))
        return [
            self._stat_card("💊", "Tổng số thuốc", len([r for r in self.rows if _is_active(r)]), "Dữ liệu theo DB hiện tại", "#2563eb"),
            self._stat_card("🧰", "Thuốc còn hàng", available, "Dữ liệu theo DB hiện tại", "#00a651"),
            self._stat_card("⚠", "Thuốc sắp hết", low, "Dữ liệu theo DB hiện tại", "#f97316"),
            self._stat_card("⛔", "Thuốc hết hàng", empty, "Dữ liệu theo DB hiện tại", "#8b5cf6"),
        ]

    def render_row(self, row, data):
        _, label = self._stock_state(data)
        self._set_item(row, 0, "☐")
        self._set_item(row, 1, row + 1)
        self._set_item(row, 2, data.get("name"))
        self._set_item(row, 3, data.get("active_ingredient") or data.get("description"))
        self._set_item(row, 4, data.get("category"))
        self._set_item(row, 5, data.get("unit") or "Viên")
        self._set_item(row, 6, data.get("supplier") or "Chưa rõ")
        self._set_item(row, 7, f"{_as_int(data.get('quantity')):,}".replace(",", "."))
        self._set_item(row, 8, _format_money(data.get("import_price") or _as_float(data.get("price")) * 0.7))
        self._set_item(row, 9, _format_money(data.get("price")))
        self.table.setCellWidget(row, 10, self._badge(label if _is_active(data) else "Ngưng hoạt động"))
        view_btn = self._icon_button("Xem", "info")
        edit_btn = self._icon_button("Sửa", "info")
        del_btn = self._icon_button("Xóa", "danger")
        view_btn.clicked.connect(lambda _, item=data: self.view_detail(item))
        edit_btn.clicked.connect(lambda _, item=data: self.edit_medicine(item))
        del_btn.clicked.connect(lambda _, item=data: self.soft_delete(item))
        self.table.setCellWidget(row, 11, self._action_cell([view_btn, edit_btn, del_btn]))

    def _medicine_fields(self):
        return [
            {"key": "medicine_code", "label": "Mã thuốc"},
            {"key": "name", "label": "Tên thuốc"},
            {"key": "active_ingredient", "label": "Hoạt chất"},
            {"key": "category", "label": "Danh mục"},
            {"key": "unit", "label": "Đơn vị"},
            {"key": "supplier", "label": "Nhà cung cấp"},
            {"key": "quantity", "label": "Số lượng", "type": "spin", "max": 1000000},
            {"key": "import_price", "label": "Giá nhập", "type": "money"},
            {"key": "price", "label": "Giá", "type": "money"},
            {"key": "description", "label": "Mô tả"},
            {"key": "is_active", "label": "Trạng thái", "type": "combo", "options": [("Hoạt động", 1), ("Ngưng", 0)]},
        ]

    def add_medicine(self):
        dialog = FormDialog("Thêm thuốc", self._medicine_fields(), {"is_active": 1, "unit": "Viên"}, self)
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return
        data = dialog.values()
        ok = _safe_execute(
            """
            INSERT INTO Medicines
            (medicine_code, name, active_ingredient, category, unit, supplier, quantity, import_price, price, description, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["medicine_code"],
                data["name"],
                data["active_ingredient"],
                data["category"],
                data["unit"],
                data["supplier"],
                data["quantity"],
                data["import_price"],
                data["price"],
                data["description"],
                data["is_active"],
            ),
        )
        self._show_info("Thuốc", "Đã thêm thuốc." if ok else "Không thể thêm thuốc.")
        self.refresh()

    def edit_medicine(self, item):
        data = dict(item)
        data["is_active"] = 1 if _is_active(item) else 0
        dialog = FormDialog("Sửa thuốc", self._medicine_fields(), data, self)
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return
        values = dialog.values()
        ok = _safe_execute(
            """
            UPDATE Medicines
            SET medicine_code=?, name=?, active_ingredient=?, category=?, unit=?, supplier=?,
                quantity=?, import_price=?, price=?, description=?, is_active=?
            WHERE medicine_id=?
            """,
            (
                values["medicine_code"],
                values["name"],
                values["active_ingredient"],
                values["category"],
                values["unit"],
                values["supplier"],
                values["quantity"],
                values["import_price"],
                values["price"],
                values["description"],
                values["is_active"],
                item.get("medicine_id"),
            ),
        )
        self._show_info("Thuốc", "Đã cập nhật thuốc." if ok else "Không thể cập nhật thuốc.")
        self.refresh()

    def soft_delete(self, item):
        if not self._confirm("Xóa thuốc", "Thuốc sẽ được ngưng hoạt động thay vì xóa cứng. Tiếp tục?"):
            return
        ok = _safe_execute("UPDATE Medicines SET is_active=0 WHERE medicine_id=?", (item.get("medicine_id"),))
        self._show_info("Thuốc", "Đã ngưng hoạt động thuốc." if ok else "Không thể cập nhật thuốc.")
        self.refresh()

    def view_detail(self, item):
        self._show_info(
            "Chi tiết thuốc",
            f"{item.get('name')}\nHoạt chất: {item.get('active_ingredient') or item.get('description')}\n"
            f"Danh mục: {item.get('category') or 'Chưa có'}\nNhà cung cấp: {item.get('supplier') or 'Chưa rõ'}\n"
            f"Tồn kho: {item.get('quantity')}\nGiá bán: {_format_money(item.get('price'))}",
        )

    def export_row(self, row):
        return [
            row.get("medicine_code") or row.get("medicine_id"),
            row.get("name"),
            row.get("active_ingredient") or row.get("description"),
            row.get("category"),
            row.get("unit"),
            row.get("supplier"),
            row.get("quantity"),
            row.get("import_price"),
            row.get("price"),
            self._stock_state(row)[1],
        ]



class PaymentManagementPage(AdminListPage):
    page_title = "Quản lý thanh toán"
    breadcrumb = "Dashboard / Quản lý thanh toán"
    headers = ["☐", "STT", "Mã giao dịch", "Bệnh nhân", "Dịch vụ/Thuốc", "Phương thức", "Số tiền", "Ngày thanh toán", "Trạng thái", "Thao tác"]
    export_headers = ["Mã giao dịch", "Bệnh nhân", "Dịch vụ/Thuốc", "Số tiền", "Phương thức", "Trạng thái", "Ngày thanh toán"]
    column_widths = [0.35, 0.45, 1.35, 1.45, 1.45, 1.05, 0.95, 1.35, 1.1, 0.9]
    search_placeholder = "Tìm kiếm (Mã giao dịch, tên bệnh nhân, dịch vụ...)"
    search_min_width = 180
    search_max_width = 260
    filter_combo_width = 128

    def _build_list_page(self):
        super()._build_list_page()
        self.table_card = self.table.parentWidget().parentWidget()
        
        self.empty_card = self._card()
        empty_layout = QtWidgets.QVBoxLayout(self.empty_card)
        empty_layout.setContentsMargins(24, 24, 24, 24)
        empty_layout.setSpacing(10)
        empty_icon = QtWidgets.QLabel("📭")
        empty_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        empty_icon.setStyleSheet("font-size: 34px;")
        self.empty_label = QtWidgets.QLabel("Chưa có thanh toán nào\nKhông tìm thấy giao dịch phù hợp với bộ lọc hiện tại.")
        self.empty_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet("font-size: 14px; font-weight: 800; color: #475569;")
        
        action_row = QtWidgets.QHBoxLayout()
        action_row.addStretch()
        add_btn = self._button("+ Thêm thanh toán", primary=True)
        add_btn.clicked.connect(self.add_payment)
        action_row.addWidget(add_btn)
        action_row.addStretch()
        
        empty_layout.addWidget(empty_icon)
        empty_layout.addWidget(self.empty_label)
        empty_layout.addLayout(action_row)
        
        self.content_layout.insertWidget(2, self.empty_card)
        self.empty_card.hide()

    def _render_table(self):
        super()._render_table()
        if not hasattr(self, "empty_card"):
            return
        if len(self.filtered_rows) == 0:
            self.empty_card.show()
            self.table_card.hide()
        else:
            self.empty_card.hide()
            self.table_card.show()

    def _add_filters(self, layout):
        self.from_date_filter = QtWidgets.QDateEdit(QtCore.QDate(2026, 5, 1))
        self.to_date_filter = QtWidgets.QDateEdit(QtCore.QDate(2026, 5, 24))
        for date_filter in [self.from_date_filter, self.to_date_filter]:
            date_filter.setCalendarPopup(True)
            date_filter.setDisplayFormat("dd/MM/yyyy")
            date_filter.setMinimumHeight(38)
            date_filter.setFixedWidth(120)
            date_filter.setStyleSheet(FormDialog._input_style())
            date_filter.dateChanged.connect(self._reset_and_refresh)
        self.method_filter = self._combo([("Tất cả", "all"), ("Tiền mặt", "Tiền mặt"), ("Chuyển khoản", "Chuyển khoản"), ("Thẻ ngân hàng", "Thẻ ngân hàng"), ("Ví điện tử", "Ví điện tử")])
        self.status_filter = self._combo([("Tất cả", "all"), ("Thành công", "paid"), ("Đang chờ", "unpaid"), ("Thất bại", "failed"), ("Hoàn tiền", "refunded"), ("Đã hủy", "cancelled")])
        layout.addWidget(self._filter_field("Từ ngày", self.from_date_filter))
        layout.addWidget(self._filter_field("Đến ngày", self.to_date_filter))
        layout.addWidget(self._filter_field("Phương thức", self.method_filter))
        layout.addWidget(self._filter_field("Trạng thái", self.status_filter))

    def _add_toolbar_buttons(self, layout):
        add_btn = self._button("Thêm thanh toán", primary=True)
        add_btn.setFixedWidth(130)
        add_btn.clicked.connect(self.add_payment)
        layout.addWidget(add_btn)
        super()._add_toolbar_buttons(layout)

    def load_rows(self):
        return _safe_fetch_all(
            """
            SELECT p.*, pa.name AS patient_name, a.appointment_date,
                   COALESCE(s.service_name, CONCAT('Lịch hẹn #', p.appointment_id)) AS service_name
            FROM Payments p
            LEFT JOIN Patients pa ON pa.patient_id = p.patient_id
            LEFT JOIN Appointments a ON a.appointment_id = p.appointment_id
            LEFT JOIN Invoices i ON i.payment_id = p.payment_id
            LEFT JOIN Services s ON s.service_id = i.service_id
            ORDER BY p.payment_date DESC
            """
        )

    def accept_row(self, row):
        parsed = _parse_date(row.get("payment_date"))
        from_qdate = self.from_date_filter.date()
        to_qdate = self.to_date_filter.date()
        start = date(from_qdate.year(), from_qdate.month(), from_qdate.day())
        end = date(to_qdate.year(), to_qdate.month(), to_qdate.day())
        date_ok = parsed is None or start <= parsed <= end
        method_ok = self.method_filter.currentData() == "all" or row.get("method") == self.method_filter.currentData()
        status_ok = self.status_filter.currentData() == "all" or row.get("status") == self.status_filter.currentData()
        return date_ok and method_ok and status_ok and _contains(
            row,
            ["payment_id", "patient_code", "patient_name", "service_name", "method", "appointment_id", "status"],
            self.search_input.text(),
        )

    def stat_cards(self):
        total = sum(_as_float(row.get("total_amount")) for row in self.rows)
        paid = sum(_as_float(row.get("total_amount")) for row in self.rows if row.get("status") == "paid")
        unpaid = sum(_as_float(row.get("total_amount")) for row in self.rows if row.get("status") == "unpaid")
        failed = sum(_as_float(row.get("total_amount")) for row in self.rows if row.get("status") == "failed")
        return [
            self._stat_card("💳", "Tổng thanh toán", _format_money(total), "Dữ liệu theo DB hiện tại", "#2563eb"),
            self._stat_card("✅", "Thanh toán thành công", _format_money(paid), "Dữ liệu theo DB hiện tại", "#00a651"),
            self._stat_card("⏳", "Đang chờ thanh toán", _format_money(unpaid), "Dữ liệu theo DB hiện tại", "#f97316"),
            self._stat_card("✕", "Thanh toán thất bại", _format_money(failed), "Dữ liệu theo DB hiện tại", "#8b5cf6"),
        ]

    def _payment_status_text(self, status):
        return {
            "paid": "Thành công",
            "unpaid": "Đang chờ",
            "failed": "Thất bại",
            "refunded": "Hoàn tiền",
            "cancelled": "Đã hủy",
        }.get(status, _as_text(status, "Đang chờ"))

    def _method_kind(self, method):
        return {"Tiền mặt": "success", "Chuyển khoản": "info", "Thẻ ngân hàng": "neutral", "Ví điện tử": "warning"}.get(method, "neutral")

    def render_row(self, row, data):
        self._set_item(row, 0, "☐")
        self._set_item(row, 1, row + 1)
        
        parsed_date = _parse_date(data.get("payment_date"))
        date_prefix = parsed_date.strftime("%d%m%y") if parsed_date else "000000"
        tx_code = f"GD{date_prefix}-{_as_int(data.get('payment_id')):04d}"
        
        self._set_item(row, 2, tx_code)
        patient_code = data.get("patient_code") or f"BN{_as_int(data.get('patient_id')):03d}"
        self._set_item(row, 3, f"👤 {data.get('patient_name') or 'Bệnh nhân'}\n{patient_code}")
        self._set_item(row, 4, data.get("service_name") or f"Lịch hẹn #{data.get('appointment_id')}")
        self.table.setCellWidget(row, 5, self._badge(data.get("method") or "Tiền mặt", self._method_kind(data.get("method"))))
        self._set_item(row, 6, _format_money(data.get("total_amount")))
        self._set_item(row, 7, _format_datetime(data.get("payment_date")))
        self.table.setCellWidget(row, 8, self._badge(self._payment_status_text(data.get("status"))))
        view_btn = self._icon_button("Xem", "info")
        print_btn = self._icon_button("In", "info")
        status_btn = self._icon_button("•••", "success")
        view_btn.clicked.connect(lambda _, item=data: self.view_detail(item))
        print_btn.clicked.connect(lambda _, item=data: self.print_invoice(item))
        status_btn.clicked.connect(lambda _, item=data: self.toggle_status(item))
        self.table.setCellWidget(row, 9, self._action_cell([view_btn, print_btn, status_btn]))

    def add_payment(self):
        patients = _safe_fetch_all("SELECT patient_id, name FROM Patients ORDER BY name")
        patient_opts = [(f"{p.get('name')} (ID: {p.get('patient_id')})", p.get("patient_id")) for p in patients] if patients else [("Không có bệnh nhân", 0)]
        
        appointments = _safe_fetch_all("SELECT appointment_id, appointment_date FROM Appointments ORDER BY appointment_date DESC LIMIT 100")
        appt_opts = [(f"Lịch hẹn #{a.get('appointment_id')} ({_format_date(a.get('appointment_date'))})", a.get("appointment_id")) for a in appointments] if appointments else [("Không có lịch hẹn", 0)]
        
        fields = [
            {"key": "patient_id", "label": "Bệnh nhân", "type": "combo", "options": patient_opts},
            {"key": "appointment_id", "label": "Lịch hẹn/Dịch vụ", "type": "combo", "options": appt_opts},
            {"key": "method", "label": "Phương thức", "type": "combo", "options": [("Tiền mặt", "Tiền mặt"), ("Chuyển khoản", "Chuyển khoản"), ("Thẻ ngân hàng", "Thẻ ngân hàng"), ("Ví điện tử", "Ví điện tử")]},
            {"key": "total_amount", "label": "Số tiền", "type": "money"},
            {"key": "status", "label": "Trạng thái", "type": "combo", "options": [("Thành công", "paid"), ("Đang chờ", "unpaid"), ("Thất bại", "failed"), ("Hoàn tiền", "refunded"), ("Đã hủy", "cancelled")]},
        ]
        dialog = FormDialog("Thêm thanh toán", fields, {"status": "unpaid", "method": "Tiền mặt"}, self)
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return
        data = dialog.values()
        
        if data["patient_id"] == 0:
            self._show_info("Lỗi", "Vui lòng chọn bệnh nhân hợp lệ.")
            return
            
        ok = _safe_execute(
            "INSERT INTO Payments (patient_id, appointment_id, total_amount, method, status) VALUES (?, ?, ?, ?, ?)",
            (data["patient_id"], data["appointment_id"], data["total_amount"], data["method"], data["status"]),
        )
        self._show_info("Thanh toán", "Đã thêm thanh toán." if ok else "Không thể thêm thanh toán.")
        self.refresh()

    def view_detail(self, item):
        parsed_date = _parse_date(item.get("payment_date"))
        date_prefix = parsed_date.strftime("%d%m%y") if parsed_date else "000000"
        tx_code = f"GD{date_prefix}-{_as_int(item.get('payment_id')):04d}"
        
        self._show_info(
            "Chi tiết thanh toán",
            f"Mã giao dịch: {tx_code}\nBệnh nhân: {item.get('patient_name')}\nDịch vụ/thuốc: {item.get('service_name') or 'Chưa có'}\n"
            f"Phương thức: {item.get('method') or 'Tiền mặt'}\nSố tiền: {_format_money(item.get('total_amount'))}\n"
            f"Trạng thái: {self._payment_status_text(item.get('status'))}\nNgày thanh toán: {_format_datetime(item.get('payment_date'))}",
        )

    def print_invoice(self, item):
        parsed_date = _parse_date(item.get("payment_date"))
        date_prefix = parsed_date.strftime("%d%m%y") if parsed_date else "000000"
        tx_code = f"GD{date_prefix}-{_as_int(item.get('payment_id')):04d}"
        
        self._show_info("In hóa đơn", f"Mã giao dịch: {tx_code}\nHóa đơn #{item.get('payment_id')}\nBệnh nhân: {item.get('patient_name')}\nDịch vụ/thuốc: {item.get('service_name') or 'Chưa có'}\nTổng tiền: {_format_money(item.get('total_amount'))}")

    def toggle_status(self, item):
        fields = [
            {"key": "status", "label": "Cập nhật trạng thái", "type": "combo", "options": [("Thành công", "paid"), ("Đang chờ", "unpaid"), ("Thất bại", "failed"), ("Hoàn tiền", "refunded"), ("Đã hủy", "cancelled")]}
        ]
        dialog = FormDialog("Cập nhật trạng thái", fields, {"status": item.get("status")}, self)
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return
            
        new_status = dialog.values()["status"]
        if new_status == item.get("status"):
            return
            
        ok = _safe_execute("UPDATE Payments SET status=? WHERE payment_id=?", (new_status, item.get("payment_id")))
        self._show_info("Thanh toán", "Đã cập nhật trạng thái." if ok else "Không thể cập nhật trạng thái.")
        self.refresh()

    def export_row(self, row):
        parsed_date = _parse_date(row.get("payment_date"))
        date_prefix = parsed_date.strftime("%d%m%y") if parsed_date else "000000"
        tx_code = f"GD{date_prefix}-{_as_int(row.get('payment_id')):04d}"
        
        return [
            tx_code,
            row.get("patient_name"),
            row.get("service_name") or row.get("appointment_id"),
            _format_money(row.get("total_amount")),
            row.get("method"),
            self._payment_status_text(row.get("status")),
            _format_datetime(row.get("payment_date")),
        ]


class ReportStatsPage(AdminBasePage):
    page_title = "Xem báo cáo thống kê"
    breadcrumb = "Dashboard / Xem báo cáo thống kê"

    def __init__(self, user_data=None, parent=None):
        super().__init__(user_data, parent)
        self._report_payload = {}
        self._status_label = None
        self._last_error = ""
        self._filter_button = None
        self._build()
        self.refresh()

    def _build(self):
        self.stats_row = QtWidgets.QHBoxLayout()
        self.stats_row.setSpacing(12)
        self.content_layout.addLayout(self.stats_row)

        filter_card = self._card()
        row = QtWidgets.QHBoxLayout(filter_card)
        row.setContentsMargins(16, 10, 16, 10)
        row.setSpacing(10)

        options = ReportController.get_filter_options()
        ranges = options.get("ranges", [])
        report_types = options.get("report_types", [])
        groups = options.get("groups", [])
        doctors = options.get("doctors", [])

        self.range_combo = QtWidgets.QComboBox()
        for item in ranges:
            self.range_combo.addItem(_as_text(item.get("label"), "30 ngày qua"), _as_int(item.get("value"), 30))

        self.report_type_combo = QtWidgets.QComboBox()
        for label in report_types:
            self.report_type_combo.addItem(label, label)
        self.report_type_combo.setEnabled(False)
        self.report_type_combo.setToolTip("Loại báo cáo nâng cao sẽ được mở ở phiên bản kế tiếp.")

        self.group_combo = QtWidgets.QComboBox()
        self.group_combo.addItem("Tất cả", "Tất cả")
        for row_group in groups:
            group_name = _as_text(row_group.get("category")).strip()
            if group_name:
                self.group_combo.addItem(group_name, group_name)

        self.doctor_combo = QtWidgets.QComboBox()
        self.doctor_combo.addItem("Tất cả", "Tất cả")
        for row_doctor in doctors:
            doctor_name = _as_text(row_doctor.get("name")).strip()
            if doctor_name:
                self.doctor_combo.addItem(f"BS. {doctor_name}", doctor_name)

        for combo, width in [
            (self.range_combo, 200),
            (self.report_type_combo, 142),
            (self.group_combo, 142),
            (self.doctor_combo, 142),
        ]:
            combo.setFixedWidth(width)
            combo.setMinimumHeight(38)
            combo.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
            combo.setStyleSheet(FormDialog._input_style())
            combo.currentIndexChanged.connect(self.refresh)
        row.addWidget(self._filter_field("Khoảng thời gian", self.range_combo))
        row.addWidget(self._filter_field("Loại báo cáo", self.report_type_combo))
        row.addWidget(self._filter_field("Nhóm", self.group_combo))
        row.addWidget(self._filter_field("Bác sĩ", self.doctor_combo))
        row.addStretch()
        self._filter_button = self._button("Lọc báo cáo", primary=True)
        self._filter_button.setFixedWidth(112)
        self._filter_button.clicked.connect(self.refresh)
        row.addWidget(self._filter_button)
        export_btn = self._button("Xuất Excel")
        export_btn.setFixedWidth(106)
        export_btn.clicked.connect(self.export_csv)
        row.addWidget(export_btn)
        self.content_layout.addWidget(filter_card)

        charts = QtWidgets.QHBoxLayout()
        charts.setSpacing(16)
        revenue_card = self._card()
        revenue_layout = QtWidgets.QVBoxLayout(revenue_card)
        revenue_layout.setContentsMargins(18, 18, 18, 18)
        revenue_layout.addWidget(self._section_title("Doanh thu theo ngày"))
        self.revenue_chart = LineChartWidget(color="#2563eb")
        self.revenue_chart.setFixedHeight(190)
        revenue_layout.addWidget(self.revenue_chart)
        charts.addWidget(revenue_card, 2)

        method_card = self._card()
        method_layout = QtWidgets.QVBoxLayout(method_card)
        method_layout.setContentsMargins(18, 18, 18, 18)
        method_layout.addWidget(self._section_title("Doanh thu theo phương thức thanh toán"))
        self.method_chart = DonutChartWidget()
        self.method_chart.setFixedHeight(190)
        method_layout.addWidget(self.method_chart)
        charts.addWidget(method_card, 1)
        self.content_layout.addLayout(charts)

        bottom = QtWidgets.QHBoxLayout()
        bottom.setSpacing(16)
        self.top_services_card = self._card()
        self.patient_stats_card = self._card()
        self.payment_status_card = self._card()
        bottom.addWidget(self.top_services_card)
        bottom.addWidget(self.patient_stats_card)
        bottom.addWidget(self.payment_status_card)
        self.content_layout.addLayout(bottom)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Mã giao dịch", "Bệnh nhân", "Dịch vụ/Thuốc", "Số tiền", "Phương thức", "Trạng thái", "Ngày thanh toán"])
        self._style_table(self.table, 12)
        self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.setFixedHeight(42 + 3 * 38)
        table_card = self._card()
        table_layout = QtWidgets.QVBoxLayout(table_card)
        table_layout.setContentsMargins(16, 16, 16, 16)
        table_layout.addWidget(self._section_title("Chi tiết giao dịch gần đây"))
        self._status_label = self._muted("")
        table_layout.addWidget(self._status_label)
        table_layout.addWidget(self.table)
        self.content_layout.addWidget(table_card)

    def _set_status_message(self, message):
        if self._status_label is not None:
            self._status_label.setText(_as_text(message))

    def _set_filter_loading(self, loading):
        if self._filter_button is None:
            return
        self._filter_button.setEnabled(not loading)
        self._filter_button.setText("Đang lọc..." if loading else "Lọc báo cáo")

    def _show_loading_state(self):
        self._set_filter_loading(True)
        self._set_status_message("Đang tải dữ liệu báo cáo...")

    def _show_error_state(self, message):
        self._set_filter_loading(False)
        self._set_status_message(f"Không thể tải báo cáo. {message}")
        self.revenue_chart.set_data([], [])
        self.method_chart.set_items([])
        self._fill_small_cards([], [], [], {
            "patient_stats": {},
            "payment_status": {},
            "top_services": [],
        })
        self._fill_table([])

    def _show_empty_state(self):
        self._set_filter_loading(False)
        self._set_status_message("Không có dữ liệu trong khoảng thời gian đã chọn")

    def _report_filters(self):
        return {
            "range_days": self.range_combo.currentData(),
            "group_name": self.group_combo.currentData() or "Tất cả",
            "doctor_name": self.doctor_combo.currentData() or "Tất cả",
        }

    def refresh(self):
        self._show_loading_state()

        filters = self._report_filters()
        try:
            payload = ReportController.get_report_stats(**filters)
            self._report_payload = payload
            self._last_error = ""
        except Exception as exc:
            self._last_error = _as_text(exc, "Lỗi không xác định")
            self._show_error_state(self._last_error)
            return

        self._set_filter_loading(False)

        summary = self._report_payload.get("summary", {})
        total_revenue = _as_float(summary.get("total_revenue"))
        total_paid = _as_float(summary.get("total_paid"))
        total_patients = _as_int(summary.get("total_patients"))
        total_services = _as_int(summary.get("total_services"))

        while self.stats_row.count():
            item = self.stats_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for card in [
            self._stat_card("💵", "Tổng doanh thu", _format_money(total_revenue), "Dữ liệu động từ DB", "#2563eb"),
            self._stat_card("✅", "Tổng thanh toán", _format_money(total_paid), "Dữ liệu động từ DB", "#00a651"),
            self._stat_card("👥", "Tổng bệnh nhân", total_patients, "Dữ liệu động từ DB", "#f97316"),
            self._stat_card("🧾", "Tổng dịch vụ", total_services, "Dữ liệu động từ DB", "#8b5cf6"),
        ]:
            self.stats_row.addWidget(card)

        daily_rows = self._report_payload.get("daily_revenue", [])
        daily_labels = [_as_text(row.get("label")) for row in daily_rows]
        daily_values = [_as_float(row.get("amount_million")) for row in daily_rows]
        self.revenue_chart.set_data(daily_labels, daily_values)

        method_rows = self._report_payload.get("payment_methods", [])
        method_items = [(_as_text(row.get("method")), _as_float(row.get("amount"))) for row in method_rows]
        self.method_chart.set_items(method_items)

        self._fill_small_cards(
            self._report_payload.get("recent_transactions", []),
            [],
            [],
            self._report_payload,
        )
        self._fill_table(self._report_payload.get("recent_transactions", []))

        if not self._report_payload.get("recent_transactions"):
            self._show_empty_state()
        else:
            self._set_status_message("Dữ liệu đã được cập nhật theo bộ lọc.")

    def _fill_small_cards(self, payments, patients, services, payload):
        for card in [self.top_services_card, self.patient_stats_card, self.payment_status_card]:
            layout = card.layout()
            if layout:
                while layout.count():
                    item = layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
            else:
                layout = QtWidgets.QVBoxLayout(card)
                layout.setContentsMargins(18, 18, 18, 18)

        self.top_services_card.layout().addWidget(self._section_title("Top dịch vụ có doanh thu cao"))
        ranking = payload.get("top_services", [])
        if ranking:
            for item in ranking:
                self.top_services_card.layout().addWidget(
                    self._muted(
                        f"{_as_int(item.get('rank'))}. {_as_text(item.get('name'))} - {_format_money(item.get('revenue'))} - {_as_int(item.get('count'))} lượt"
                    )
                )
        else:
            self.top_services_card.layout().addWidget(self._muted("Chưa có dữ liệu"))

        self.patient_stats_card.layout().addWidget(self._section_title("Thống kê bệnh nhân"))
        patient_stats = payload.get("patient_stats", {})
        patient_lines = [
            ("Tổng bệnh nhân", str(_as_int(patient_stats.get("total")))),
            ("Bệnh nhân mới", str(_as_int(patient_stats.get("new")))),
            ("Bệnh nhân tái khám", str(_as_int(patient_stats.get("returning")))),
            ("Nam", str(_as_int(patient_stats.get("male")))),
            ("Nữ", str(_as_int(patient_stats.get("female")))),
        ]
        for label, value in patient_lines:
            self.patient_stats_card.layout().addWidget(self._muted(f"{label}: {value}"))

        self.payment_status_card.layout().addWidget(self._section_title("Tình trạng thanh toán"))
        status_payload = payload.get("payment_status", {})
        status_lines = [
            (f"Thành công: {_as_int(status_payload.get('paid'))}", "success"),
            (f"Đang chờ: {_as_int(status_payload.get('unpaid'))}", "warning"),
            (f"Thất bại: {_as_int(status_payload.get('failed'))}", "danger"),
            (f"Khác: {_as_int(status_payload.get('other'))}", "neutral"),
        ]
        for text, kind in status_lines:
            self.payment_status_card.layout().addWidget(self._badge(text, kind))

    def _fill_table(self, payments):
        self.table.setRowCount(len(payments))
        for row, item in enumerate(payments):
            parsed_date = _parse_date(item.get("payment_date"))
            date_prefix = parsed_date.strftime("%d%m%y") if parsed_date else "000000"
            tx_code = f"GD{date_prefix}-{_as_int(item.get('payment_id')):04d}"
            for column, value in enumerate([
                tx_code,
                item.get("patient_name"),
                item.get("service_name") or item.get("appointment_id"),
                _format_money(item.get("total_amount")),
                item.get("method") or "Tiền mặt",
                {"paid": "Thành công", "unpaid": "Đang chờ", "failed": "Thất bại"}.get(item.get("status"), item.get("status")),
                _format_datetime(item.get("payment_date")),
            ]):
                self.table.setItem(row, column, QtWidgets.QTableWidgetItem(_as_text(value)))
            self.table.setRowHeight(row, 38)

    def export_csv(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Xuất báo cáo", "bao_cao_thong_ke.csv", "CSV Files (*.csv)")
        if not path:
            return
        payments = self._report_payload.get("recent_transactions", [])
        with open(path, "w", newline="", encoding="utf-8-sig") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["payment_id", "patient_name", "service_name", "total_amount", "method", "payment_date", "status"])
            for row in payments:
                writer.writerow([row.get("payment_id"), row.get("patient_name"), row.get("service_name"), row.get("total_amount"), row.get("method"), row.get("payment_date"), row.get("status")])
        self._show_info("Xuất báo cáo", "Đã xuất báo cáo theo bộ lọc.")


class RolePermissionPage(AdminBasePage):
    page_title = "Phân quyền hệ thống"
    breadcrumb = "Dashboard / Phân quyền hệ thống"
    PERMISSIONS = {
        "Quản lý hệ thống": ["Quản lý người dùng", "Phân quyền người dùng", "Quản lý vai trò", "Cấu hình hệ thống", "Sao lưu dữ liệu", "Nhật ký hệ thống"],
        "Quản lý bác sĩ": ["Xem danh sách bác sĩ", "Thêm bác sĩ", "Sửa thông tin bác sĩ", "Xóa bác sĩ", "Quản lý lịch làm việc"],
        "Quản lý bệnh nhân": ["Xem danh sách bệnh nhân", "Thêm bệnh nhân", "Sửa thông tin bệnh nhân", "Xóa bệnh nhân", "Xem lịch sử khám"],
        "Quản lý thuốc": ["Xem danh sách thuốc", "Thêm thuốc", "Sửa thông tin thuốc", "Xóa thuốc"],
        "Quản lý dịch vụ": ["Xem dịch vụ", "Thêm dịch vụ", "Sửa dịch vụ", "Ngừng cung cấp dịch vụ"],
        "Quản lý thanh toán": ["Xem thanh toán", "Cập nhật trạng thái", "In hóa đơn", "Hoàn tiền", "Xuất báo cáo"],
        "Báo cáo thống kê": ["Xem dashboard báo cáo", "Lọc báo cáo", "Xuất Excel", "Xem doanh thu", "Xem thống kê bệnh nhân"],
        "Sao lưu dữ liệu": ["Xem backup", "Tạo backup", "Tải backup", "Xóa backup", "Khôi phục dữ liệu"],
        "Quản lý tài khoản": ["Tạo tài khoản", "Khóa tài khoản", "Reset mật khẩu", "Gán vai trò", "Xem lịch sử đăng nhập"],
        "Quản lý phân quyền": ["Thêm vai trò", "Sửa vai trò", "Gán quyền", "Thu hồi quyền"],
    }
    ROLE_INFO = {
        "admin": ("⚙", "Quản trị viên", "Toàn quyền hệ thống", "success"),
        "doctor": ("👨‍⚕️", "Bác sĩ", "Quản lý chuyên môn", "info"),
        "staff": ("👥", "Nhân viên", "Vận hành và hỗ trợ", "warning"),
        "patient": ("🧑", "Khách hàng", "Sử dụng dịch vụ khám", "neutral"),
    }

    def __init__(self, user_data=None, parent=None):
        super().__init__(user_data, parent)
        self.selected_role = "admin"
        self._build()
        self.refresh()

    def _build(self):
        user_count = len(_safe_fetch_all("SELECT user_id FROM Users"))
        role_count = len(self.ROLE_INFO)
        permission_count = sum(len(values) for values in self.PERMISSIONS.values())
        permission_groups = len(self.PERMISSIONS)
        stats = QtWidgets.QHBoxLayout()
        stats.setSpacing(12)
        stats.addWidget(self._stat_card("🛡", "Tổng vai trò", role_count, "vai trò trong hệ thống", "#00a651"))
        stats.addWidget(self._stat_card("👥", "Tổng người dùng", user_count, "người dùng đã phân quyền", "#2563eb"))
        stats.addWidget(self._stat_card("🔑", "Tổng quyền", permission_count, "quyền trong hệ thống", "#f97316"))
        stats.addWidget(self._stat_card("◔", "Nhóm quyền", permission_groups, "nhóm quyền chức năng", "#8b5cf6"))
        self.content_layout.addLayout(stats)

        actions = QtWidgets.QHBoxLayout()
        self.role_tab = self._badge("Quản lý vai trò", "success")
        self.user_tab = self._badge("Quản lý người dùng", "neutral")
        actions.addWidget(self.role_tab)
        actions.addWidget(self.user_tab)
        actions.addStretch()
        add_role = self._button("Thêm vai trò", primary=True)
        add_role.clicked.connect(lambda: self._show_info("Thêm vai trò", "Mở form tạo vai trò mới khi có schema phân quyền động."))
        actions.addWidget(add_role)
        cfg = self._button("Cấu hình quyền", primary=True)
        cfg.clicked.connect(lambda: self._show_info("Cấu hình quyền", "Hệ thống đang dùng phân quyền theo role trong bảng Users."))
        actions.addWidget(cfg)
        self.content_layout.addLayout(actions)

        main = QtWidgets.QHBoxLayout()
        main.setSpacing(16)
        left = self._card()
        left_layout = QtWidgets.QVBoxLayout(left)
        left_layout.setContentsMargins(16, 16, 16, 16)
        left_layout.addWidget(self._section_title("Danh sách vai trò"))
        role_search = QtWidgets.QLineEdit()
        role_search.setPlaceholderText("Tìm kiếm vai trò...")
        role_search.setMinimumHeight(38)
        role_search.setStyleSheet(FormDialog._input_style())
        left_layout.addWidget(role_search)
        self.role_list = QtWidgets.QListWidget()
        self.role_list.setStyleSheet("""
            QListWidget { border: none; background: white; }
            QListWidget::item { padding: 12px; border-radius: 10px; color: #0f172a; }
            QListWidget::item:selected { background: #e8f7ef; color: #00a651; border-left: 3px solid #00a651; }
        """)
        self.role_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.role_list.currentTextChanged.connect(self._role_changed)
        left_layout.addWidget(self.role_list)
        main.addWidget(left, 1)

        right = self._card()
        right_layout = QtWidgets.QVBoxLayout(right)
        right_layout.setContentsMargins(16, 16, 16, 16)
        self.permission_title = self._section_title("Danh sách quyền")
        right_layout.addWidget(self.permission_title)
        self.permission_subtitle = self._muted("")
        right_layout.addWidget(self.permission_subtitle)
        self.permission_table = QtWidgets.QTableWidget()
        self.permission_table.setColumnCount(4)
        self.permission_table.setHorizontalHeaderLabels(["Nhóm quyền", "Danh sách quyền", "Mô tả", "Trạng thái"])
        self._style_table(self.permission_table, 12)
        self.permission_table.setWordWrap(True)
        self.permission_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.permission_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.permission_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.permission_table.setFixedHeight(560)
        right_layout.addWidget(self.permission_table)
        main.addWidget(right, 2)
        self.content_layout.addLayout(main)

    def refresh(self):
        role_counts = {row.get("role"): _as_int(row.get("count")) for row in _safe_fetch_all("SELECT role, COUNT(*) AS count FROM Users GROUP BY role")}
        self.role_list.clear()
        for role, (icon, name, description, _kind) in self.ROLE_INFO.items():
            users = f"{role_counts.get(role, 0)} người dùng"
            item = QtWidgets.QListWidgetItem(f"{icon}  {name}\n   {description}                                      {users}")
            item.setSizeHint(QtCore.QSize(0, 62))
            item.setData(QtCore.Qt.ItemDataRole.UserRole, role)
            self.role_list.addItem(item)
        self.role_list.setCurrentRow(0)

    def _role_changed(self, _text=None):
        item = self.role_list.currentItem()
        if item:
            self.selected_role = item.data(QtCore.Qt.ItemDataRole.UserRole)
        self._fill_permissions()

    def _fill_permissions(self):
        role = self.selected_role
        role_counts = {row.get("role"): _as_int(row.get("count")) for row in _safe_fetch_all("SELECT role, COUNT(*) AS count FROM Users GROUP BY role")}
        _icon, role_name, description, _kind = self.ROLE_INFO.get(role, ("", "Quản trị viên", "Toàn quyền hệ thống", "success"))
        users = f"{role_counts.get(role, 0)} người dùng"
        self.permission_title.setText(f"Danh sách quyền của vai trò: {role_name}")
        self.permission_subtitle.setText(f"{description}                         {users}")
        rows = list(self.PERMISSIONS.items())
        row_count = sum(len(permissions) for _group, permissions in rows)
        self.permission_table.setRowCount(row_count)
        table_row = 0
        for group, permissions in rows:
            allowed = self.selected_role == "admin" or group not in {"Quản lý hệ thống"}
            for index, permission in enumerate(permissions):
                group_text = f"⌄  {group}\n   {len(permissions)} quyền" if index == 0 else ""
                self.permission_table.setItem(table_row, 0, QtWidgets.QTableWidgetItem(group_text))
                self.permission_table.setItem(table_row, 1, QtWidgets.QTableWidgetItem(permission))
                self.permission_table.setItem(table_row, 2, QtWidgets.QTableWidgetItem(self._permission_description(group, permission)))
                self.permission_table.setCellWidget(table_row, 3, self._badge("Được phép" if allowed else "Không được phép", "success" if allowed else "danger"))
                self.permission_table.setRowHeight(table_row, 50 if index == 0 else 34)
                table_row += 1
        self.permission_table.setFixedHeight(min(560, 42 + row_count * 34 + len(rows) * 16))

    def _permission_description(self, group, permission):
        lowered = permission.lower()
        if lowered.startswith("xem"):
            return f"Xem thông tin trong module {group.lower()}"
        if lowered.startswith("thêm") or lowered.startswith("tạo"):
            return f"Thêm mới dữ liệu trong module {group.lower()}"
        if lowered.startswith("sửa") or lowered.startswith("cập nhật"):
            return f"Cập nhật thông tin trong module {group.lower()}"
        if lowered.startswith("xóa") or lowered.startswith("thu hồi"):
            return f"Xóa hoặc thu hồi quyền trong module {group.lower()}"
        return f"Quyền thao tác module {group.lower()}"


class BackupManagementPage(AdminBasePage):
    page_title = "Sao lưu dữ liệu"
    breadcrumb = "Dashboard / Sao lưu dữ liệu"

    def __init__(self, user_data=None, parent=None):
        super().__init__(user_data, parent)
        self.backups_root = Path(__file__).resolve().parents[1] / "backups"
        self._build()
        self.refresh()

    def _build(self):
        self.stats_row = QtWidgets.QHBoxLayout()
        self.stats_row.setSpacing(12)
        self.content_layout.addLayout(self.stats_row)

        main = QtWidgets.QHBoxLayout()
        main.setSpacing(16)
        left = QtWidgets.QVBoxLayout()
        now_card = self._card()
        now_layout = QtWidgets.QVBoxLayout(now_card)
        now_layout.setContentsMargins(18, 18, 18, 18)
        now_layout.addWidget(self._section_title("Sao lưu dữ liệu ngay"))
        now_layout.addWidget(self._muted("Tạo bản sao lưu mới cho toàn bộ hệ thống. Quá trình sao lưu có thể mất vài phút tùy theo dung lượng dữ liệu."))
        self.ready_box = self._badge("Hệ thống sẵn sàng để sao lưu", "success")
        now_layout.addWidget(self.ready_box)
        now_layout.addWidget(self._muted("Tất cả dữ liệu sẽ được sao lưu an toàn."))
        action_row = QtWidgets.QHBoxLayout()
        self.mode_combo = QtWidgets.QComboBox()
        self.mode_combo.addItem("Cloud", "cloud")
        self.mode_combo.addItem("Local", "local")
        self.mode_combo.setStyleSheet(FormDialog._input_style())
        backup_btn = self._button("Sao lưu ngay", primary=True)
        backup_btn.clicked.connect(self.backup_now)
        advanced_btn = self._button("Tùy chọn nâng cao")
        advanced_btn.clicked.connect(lambda: self._show_info("Tùy chọn nâng cao", "Hiện hỗ trợ chọn Cloud/Local; các tùy chọn mở rộng phụ thuộc hạ tầng lưu trữ."))
        action_row.addWidget(self.mode_combo)
        action_row.addWidget(backup_btn)
        action_row.addWidget(advanced_btn)
        action_row.addStretch()
        now_layout.addLayout(action_row)
        left.addWidget(now_card)

        history_card = self._card()
        history_layout = QtWidgets.QVBoxLayout(history_card)
        history_layout.setContentsMargins(18, 18, 18, 18)
        history_title = QtWidgets.QHBoxLayout()
        history_title.addWidget(self._section_title("Lịch sử sao lưu"))
        history_title.addStretch()
        history_title.addWidget(self._badge("Xem tất cả", "info"))
        history_layout.addLayout(history_title)
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Thời gian", "Loại", "Dung lượng", "Người tạo", "Trạng thái", "Thao tác"])
        self._style_table(self.table, 12)
        self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.setFixedHeight(42 + 7 * 44)
        history_layout.addWidget(self.table)
        left.addWidget(history_card)
        main.addLayout(left, 2)

        right = QtWidgets.QVBoxLayout()
        self.info_card = self._card()
        self.options_card = self._card()
        self.restore_card = self._card()
        for card in [self.info_card, self.options_card, self.restore_card]:
            right.addWidget(card)
        right.addStretch()
        main.addLayout(right, 1)
        self.content_layout.addLayout(main)

    def _backup_files(self):
        files = []
        for mode in ["local", "cloud"]:
            folder = self.backups_root / mode
            if not folder.exists():
                continue
            for path in folder.glob("*.json"):
                stat = path.stat()
                files.append({"path": path, "mode": mode, "size": stat.st_size, "mtime": datetime.fromtimestamp(stat.st_mtime)})
        return sorted(files, key=lambda item: item["mtime"], reverse=True)

    def refresh(self):
        files = self._backup_files()
        total_size = sum(item["size"] for item in files)
        last = files[0]["mtime"].strftime("%d/%m/%Y %H:%M") if files else "Chưa có"
        while self.stats_row.count():
            item = self.stats_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for card in [
            self._stat_card("🗄", "Tổng dung lượng dữ liệu", self._backup_size_text(total_size), "Tính trên toàn bộ dữ liệu sao lưu", "#2563eb"),
            self._stat_card("☁", "Bản sao lưu gần nhất", last, "Sao lưu dữ liệu hoàn tất", "#00a651"),
            self._stat_card("🕑", "Lịch sao lưu tự động", "02:00 AM", "Hàng ngày", "#f97316"),
            self._stat_card("🛡", "Trạng thái hệ thống", "An toàn" if files else "Cảnh báo", "Dữ liệu được bảo vệ", "#8b5cf6"),
        ]:
            self.stats_row.addWidget(card)
        self._fill_table(files)
        self._fill_side_cards(files, total_size)

    def _backup_size_text(self, size):
        if size >= 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024 * 1024):.1f} GB"
        if size >= 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"
        return f"{size / 1024:.1f} KB"

    def _fill_table(self, files):
        self.table.setRowCount(len(files))
        for row, item in enumerate(files):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(item["mtime"].strftime("%d/%m/%Y %H:%M")))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(_as_text(item["mode"]).title()))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(item.get("size_text") or self._backup_size_text(item["size"])))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(item.get("creator") or "Hệ thống"))
            self.table.setCellWidget(row, 4, self._badge("Thành công", "success"))
            download = self._icon_button("Tải", "info")
            delete = self._icon_button("Xóa", "danger")
            download.clicked.connect(lambda _, file_item=item: self.download_backup(file_item))
            delete.clicked.connect(lambda _, file_item=item: self.delete_backup(file_item))
            self.table.setCellWidget(row, 5, self._action_cell([download, delete]))
            self.table.setRowHeight(row, 44)

    def _fill_side_cards(self, files, total_size):
        specs = [
            (self.info_card, "Thông tin sao lưu", [
                "Vị trí lưu trữ: Máy chủ nội bộ",
                "Đường dẫn: /backup/careplus/",
                f"Tổng số bản sao lưu: {len(files)} bản",
                f"Bản sao lưu gần nhất: {files[0]['mtime'].strftime('%d/%m/%Y %H:%M') if files else 'Chưa có'}",
                f"Bản sao lưu tiếp theo: {(datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y')} 02:00",
                "Phương thức: Tự động hằng ngày",
                "Giữ lại bản sao lưu: 30 ngày",
            ]),
            (self.options_card, "Tùy chọn sao lưu", [
                "Sao lưu tự động: Bật",
                "Sao lưu cơ sở dữ liệu: Bật",
                "Sao lưu tệp đính kèm: Bật",
                "Nén dữ liệu: Bật",
                "Gửi email thông báo: Tắt",
            ]),
            (self.restore_card, "Khôi phục dữ liệu", ["Khôi phục dữ liệu từ bản sao lưu đã chọn.", "Bạn nên tạo bản sao lưu hiện tại trước khi khôi phục."]),
        ]
        for card, title, lines in specs:
            layout = card.layout()
            if layout:
                while layout.count():
                    item = layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
            else:
                layout = QtWidgets.QVBoxLayout(card)
                layout.setContentsMargins(18, 18, 18, 18)
            layout.addWidget(self._section_title(title))
            for line in lines:
                if card is self.options_card:
                    row = QtWidgets.QHBoxLayout()
                    label, _, state = line.partition(":")
                    row.addWidget(self._muted(label))
                    row.addStretch()
                    row.addWidget(self._badge(state.strip(), "success" if state.strip() == "Bật" else "neutral"))
                    layout.addLayout(row)
                else:
                    layout.addWidget(self._muted(line))
            if card is self.restore_card:
                restore_btn = self._button("Chọn bản sao lưu để khôi phục", danger=True)
                restore_btn.clicked.connect(lambda: self._show_info("Khôi phục dữ liệu", "Restore thật đang bị khóa để tránh mất dữ liệu ngoài ý muốn."))
                layout.addWidget(restore_btn)
            layout.addStretch()

    def backup_now(self):
        user_id = self.user_data.get("user_id") or 1
        mode = self.mode_combo.currentData() or "local"
        if not self._confirm("Sao lưu dữ liệu", "Bạn có chắc muốn tạo bản sao lưu mới?"):
            return
        ok, result = SettingsController.backup_now(user_id, mode)
        self._show_info("Sao lưu dữ liệu", f"Sao lưu thành công.\n{result}" if ok else _as_text(result, "Không thể sao lưu."))
        self.refresh()

    def download_backup(self, item):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Chọn thư mục lưu bản sao")
        if not folder:
            return
        destination = Path(folder) / item["path"].name
        shutil.copy2(item["path"], destination)
        self._show_info("Tải bản sao lưu", f"Đã sao chép tới:\n{destination}")

    def delete_backup(self, item):
        if not self._confirm("Xóa backup", f"Xóa bản sao lưu {item['path'].name}? Thao tác này không thể hoàn tác."):
            return
        item["path"].unlink(missing_ok=True)
        self.refresh()


    def _sync_doctor_filter(self):
        current = self.doctor_combo.currentData() if hasattr(self, "doctor_combo") else "Tất cả"
        doctors = _safe_fetch_all("SELECT name FROM Doctors WHERE is_active=1 ORDER BY name ASC")
        self.doctor_combo.blockSignals(True)
        self.doctor_combo.clear()
        self.doctor_combo.addItem("Tất cả", "Tất cả")
        for row in doctors:
            name = _as_text(row.get("name")).strip()
            if name:
                self.doctor_combo.addItem(f"BS. {name}", name)
        idx = self.doctor_combo.findData(current)
        self.doctor_combo.setCurrentIndex(max(idx, 0))
        self.doctor_combo.blockSignals(False)


class AppointmentManagementView(AdminListPage):
    page_title = "Quản lý lịch hẹn"
    breadcrumb = "Dashboard / Quản lý lịch hẹn"
    headers = ["ID", "Bệnh nhân", "Bác sĩ", "Ngày hẹn", "Trạng thái", "Thao tác"]
    search_placeholder = "Tìm kiếm lịch hẹn..."

    def _add_filters(self, layout):
        self.status_filter = self._combo([
            ("Tất cả trạng thái", "all"),
            ("Chờ xác nhận", "pending"),
            ("Đã xác nhận", "confirmed"),
            ("Đang khám", "in_progress"),
            ("Hoàn tất", "done"),
            ("Đã hủy", "cancelled"),
        ])
        layout.addWidget(self.status_filter)

    def load_rows(self):
        return _safe_fetch_all(
            """
            SELECT a.*, p.name AS patient_name, d.name AS doctor_name
            FROM Appointments a
            LEFT JOIN Patients p ON p.patient_id = a.patient_id
            LEFT JOIN Doctors d ON d.doctor_id = a.doctor_id
            ORDER BY a.appointment_date DESC
            """
        )

    def accept_row(self, row):
        status_ok = self.status_filter.currentData() == "all" or row.get("status") == self.status_filter.currentData()
        return status_ok and _contains(row, ["appointment_id", "patient_name", "doctor_name", "status"], self.search_input.text())

    def stat_cards(self):
        pending = sum(1 for row in self.rows if row.get("status") == "pending")
        done = sum(1 for row in self.rows if row.get("status") == "done")
        cancelled = sum(1 for row in self.rows if row.get("status") == "cancelled")
        return [
            self._stat_card("📅", "Tổng lịch hẹn", len(self.rows), "Tất cả trạng thái", "#2563eb"),
            self._stat_card("⏳", "Chờ xác nhận", pending, "status = pending", "#f97316"),
            self._stat_card("✅", "Hoàn tất", done, "status = done", "#00a651"),
            self._stat_card("🚫", "Đã hủy", cancelled, "status = cancelled", "#ef4444"),
        ]

    def render_row(self, row, data):
        self._set_item(row, 0, data.get("appointment_id"))
        self._set_item(row, 1, data.get("patient_name") or f"BN #{data.get('patient_id')}")
        self._set_item(row, 2, data.get("doctor_name") or f"BS #{data.get('doctor_id')}")
        self._set_item(row, 3, _format_datetime(data.get("appointment_date")))
        self.table.setCellWidget(row, 4, self._badge(_as_text(data.get("status"))))
        cancel_btn = self._icon_button("Hủy", "danger")
        cancel_btn.clicked.connect(lambda _, item=data: self.cancel_appointment(item))
        self.table.setCellWidget(row, 5, self._action_cell([cancel_btn]))

    def cancel_appointment(self, item):
        if not self._confirm("Hủy lịch hẹn", "Chuyển lịch hẹn sang trạng thái cancelled?"):
            return
        ok = _safe_execute("UPDATE Appointments SET status='cancelled' WHERE appointment_id=?", (item.get("appointment_id"),))
        self._show_info("Lịch hẹn", "Đã hủy lịch hẹn." if ok else "Không thể cập nhật lịch hẹn.")
        self.refresh()

    def export_row(self, row):
        return [row.get("appointment_id"), row.get("patient_name"), row.get("doctor_name"), row.get("appointment_date"), row.get("status")]


from views.service_management_view import ServiceManagementPage
class CarePlusAdminDashboard(QtWidgets.QWidget):
    MENU = [
        ("🏠", "Dashboard", AdminHomePage),
        ("👥", "Quản lý tài khoản", AccountManagementPage),
        ("👨‍⚕️", "Quản lý bác sĩ", DoctorManagementPage),
        ("🧑", "Quản lý bệnh nhân", PatientManagementPage),
        ("💊", "Quản lý thuốc", MedicineManagementPage),
        ("🧾", "Quản lý dịch vụ", ServiceManagementPage),
        ("💳", "Quản lý thanh toán", PaymentManagementPage),
        ("📊", "Xem báo cáo thống kê", ReportStatsPage),
        ("🛡️", "Phân quyền hệ thống", RolePermissionPage),
        ("💾", "Sao lưu dữ liệu", BackupManagementPage),
    ]

    def __init__(self, user_data=None, parent=None):
        super().__init__(parent)
        self.user_data = user_data or {"role": "admin"}
        self.nav_buttons = []
        self._build_shell()
        self.switch_page(0)

    def _build_shell(self):
        root = QtWidgets.QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        sidebar = QtWidgets.QFrame()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet("background: white; border-right: 1px solid #e2e8f0;")
        side_layout = QtWidgets.QVBoxLayout(sidebar)
        side_layout.setContentsMargins(16, 26, 16, 24)
        side_layout.setSpacing(8)

        logo = QtWidgets.QWidget()
        logo_layout = QtWidgets.QHBoxLayout(logo)
        logo_layout.setContentsMargins(6, 0, 0, 18)
        logo_layout.setSpacing(10)
        logo_icon = QtWidgets.QLabel("+")
        logo_icon.setFixedSize(30, 30)
        logo_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        logo_icon.setStyleSheet("background: #00a651; color: white; border-radius: 15px; font-size: 24px; font-weight: 950;")
        logo_text = QtWidgets.QLabel("CarePlus Admin")
        logo_text.setStyleSheet("color: #00a651; font-size: 22px; font-weight: 950; background: transparent;")
        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()
        side_layout.addWidget(logo)

        for index, (icon, text, _) in enumerate(self.MENU):
            btn = QtWidgets.QPushButton(f"  {icon}   {text}")
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.clicked.connect(lambda _, idx=index: self.switch_page(idx))
            self.nav_buttons.append(btn)
            side_layout.addWidget(btn)
        side_layout.addStretch()
        self.btn_logout = QtWidgets.QPushButton("  🚪   Đăng xuất")
        self.btn_logout.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_logout.setStyleSheet("""
            QPushButton {
                border: none;
                text-align: left;
                padding: 12px 14px;
                color: #dc2626;
                background: #fee2e2;
                border-radius: 10px;
                font-weight: 900;
            }
        """)
        side_layout.addWidget(self.btn_logout)
        root.addWidget(sidebar)

        main = QtWidgets.QWidget()
        main.setStyleSheet(f"background: {PAGE_BG};")
        main_layout = QtWidgets.QVBoxLayout(main)
        main_layout.setContentsMargins(24, 24, 24, 28)
        main_layout.setSpacing(18)

        header = QtWidgets.QHBoxLayout()
        title_box = QtWidgets.QVBoxLayout()
        title_box.setSpacing(3)
        self.title_label = QtWidgets.QLabel()
        self.title_label.setStyleSheet("font-size: 30px; color: #0f172a; font-weight: 950;")
        self.breadcrumb_label = QtWidgets.QLabel()
        self.breadcrumb_label.setStyleSheet("font-size: 13px; color: #64748b; font-weight: 700;")
        title_box.addWidget(self.title_label)
        title_box.addWidget(self.breadcrumb_label)
        header.addLayout(title_box)
        header.addStretch()
        bell = QtWidgets.QFrame()
        bell.setObjectName("adminBell")
        bell.setFixedSize(44, 40)
        bell.setStyleSheet("""
            QFrame#adminBell {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 20px;
            }
        """)
        bell_icon = QtWidgets.QLabel("🔔", bell)
        bell_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        bell_icon.setGeometry(8, 9, 28, 24)
        bell_icon.setStyleSheet("background: transparent; color: #0f172a; font-size: 15px;")
        bell_badge = QtWidgets.QLabel("3", bell)
        bell_badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        bell_badge.setGeometry(27, 2, 16, 16)
        bell_badge.setStyleSheet("background: #ef4444; color: white; border-radius: 8px; font-size: 10px; font-weight: 900;")
        header.addWidget(bell)
        user_name = self.user_data.get("name") or self.user_data.get("username") or "Quản trị viên"
        user = QtWidgets.QFrame()
        user.setObjectName("adminUserPill")
        user.setStyleSheet("""
            QFrame#adminUserPill {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 20px;
            }
            QLabel { background: transparent; }
        """)
        user_layout = QtWidgets.QHBoxLayout(user)
        user_layout.setContentsMargins(7, 0, 13, 0)
        user_layout.setSpacing(8)
        avatar = QtWidgets.QLabel("👨‍💼")
        avatar.setFixedSize(30, 30)
        avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("background: #eff6ff; border-radius: 15px; font-size: 17px;")
        user_text = QtWidgets.QLabel(f"{user_name} (Quản trị viên) ▾")
        user_text.setStyleSheet("color: #0f172a; font-weight: 850; font-size: 12px;")
        user_layout.addWidget(avatar)
        user_layout.addWidget(user_text)
        user.setFixedHeight(40)
        header.addWidget(user)
        main_layout.addLayout(header)

        self.stack = QtWidgets.QStackedWidget()
        self.pages = []
        for _, _, page_cls in self.MENU:
            page = page_cls(self.user_data)
            self.pages.append(page)
            scroll = QtWidgets.QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
            scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scroll.setWidget(page)
            self.stack.addWidget(scroll)
        main_layout.addWidget(self.stack)
        root.addWidget(main)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)
        page = self.pages[index]
        self.title_label.setText(page.page_title)
        self.breadcrumb_label.setText(page.breadcrumb)
        for i, btn in enumerate(self.nav_buttons):
            active = i == index
            btn.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    text-align: left;
                    padding: 12px 14px;
                    border-radius: 10px;
                    font-size: 13px;
                    color: {'#00a651' if active else '#1e293b'};
                    background: {'#e8f7ef' if active else 'transparent'};
                    font-weight: {'950' if active else '750'};
                }}
                QPushButton:hover {{ background: #f1f5f9; }}
            """)


PatientManagementView = PatientManagementPage
DoctorManagementView = DoctorManagementPage
MedicineManagementView = MedicineManagementPage
ServiceManagementView = ServiceManagementPage
PaymentManagementView = PaymentManagementPage
ReportStatsView = ReportStatsPage
