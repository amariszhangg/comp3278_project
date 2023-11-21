from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QMainWindow, QMessageBox, QLabel
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QScrollArea, QSizePolicy
from PyQt5.QtGui import QIcon, QFont, QDesktopServices, QCursor
from PyQt5.QtCore import Qt, QVariantAnimation, QEasingCurve, QUrl, QSize

import database
import data

import datetime
from dataclasses import dataclass

from typing import List

@dataclass
class Course:
    courseCode: str
    teacherId: int
    courseName: str
    zoomLink: str
    courseDescription: str

class CourseWidget(QStackedWidget):
    def __init__(self):
        super().__init__()
        # self.init_UI()

    def init_UI(self):
        while self.count() > 0:
            widget = self.widget(0)
            self.removeWidget(widget)
            widget.deleteLater()

        self.main_layout = QVBoxLayout()

        self.courses: List[Course] = []
        for course_code in database.getEnrolled(data.student_id):
            if course_code is not None:
                course_data = database.getCourse(course_code)
                course = Course(
                    courseCode=course_data[0],
                    teacherId=course_data[1],
                    courseName=course_data[2],
                    zoomLink=course_data[3],
                    courseDescription=course_data[4]
                )
                self.courses.append(course)
        self.course_code_to_subpage_idx: dict[str, int] = {}
        idx = 0
        for course in self.courses:
            self.course_code_to_subpage_idx[course.courseCode] = idx
            idx += 1
            
            course_widget = CourseEntityWidget(course)
            self.main_layout.addWidget(course_widget)
        self.main_layout.addStretch(1)

        self.scroll_content = QWidget()
        self.scroll_content.setLayout(self.main_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setWidget(self.scroll_content)

        self.addWidget(self.scroll_area)
        self.main_page_idx = idx

        self.switch_main_page()

    def switch_detail_page(self, courseCode: str):
        self.setCurrentIndex(self.course_code_to_subpage_idx[courseCode])
    
    def switch_main_page(self):
        self.setCurrentIndex(self.main_page_idx)


# course_widget = QWidget()
# course_layout = QVBoxLayout()
# course_layout.setAlignment(Qt.AlignCenter)

# courses: List[Course] = []
# for course_code in database.getEnrolled(data.student_id):
#     if course_code is not None:
#         course_data = database.getCourse(course_code)
#         course = Course(
#             courseCode=course_data[0],
#             teacherId=course_data[1],
#             courseName=course_data[2],
#             zoomLink=course_data[3],
#             courseDescription=course_data[4]
#         )
#         courses.append(course)

# for course in courses:
#     course_widget = CourseEntityWidget(course)
#     course_layout.addWidget(course_widget)
# course_layout.addStretch(1)

# scroll_content = QWidget()
# scroll_content.setLayout(course_layout)

# scroll_area = QScrollArea()
# scroll_area.setWidgetResizable(True)
# scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
# scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
# scroll_area.setWidget(scroll_content)

# course_layout.addWidget(scroll_area)

class CourseEntityWidget(QWidget):
    def __init__(self, course: Course):
        super().__init__()
        self.course = course
        self.init_UI()

    def init_UI(self):
        self.main_layout = QVBoxLayout()

        self.down_button = QPushButton(QIcon("assets/chevron_down.png"), f"{self.course.courseCode}: {self.course.courseName}")
        self.down_botton.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.down_button.setFlat(True)
        self.button_stylesheet = '''
            QPushButton {
                background-color: #AAC4FF; 
                border: 2px #B1B2FF;
                border-radius: 5px; 
                border-style: none solid solid none;
                padding: 10px 20px;
                color: #ffffff; 
                font-family: ubuntu, arial; 
                font-size: 20px;
            } 
            
            QPushButton:hover {
                background-color: #C6D0FF;
                border: 0;
            }
        '''

        self.content_stylesheet = '''
            QLabel {
                font-size: 20px;
                padding-left: 30px;
                margin-bottom: 20px;
            }
        '''
        self.down_button.setStyleSheet(self.btn_stylesheet)
        self.down_button.clicked.connect(self.expand_entity)

        self.expand_layout = QVBoxLayout()

        self.description_label = QLabel(f"Course Description:\n\t{self.course.courseDescription}")
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet(self.content_stylesheet)
        self.description_label.adjustSize()

        teachers_info = database.getTeachersForCourse(self.course.courseCode)
        self.teacher_label = QLabel(
            "Teacher:" + 
            "".join(
                f"\n\tName: {teacher_info[0]}\n\tEmail: {teacher_info[1]}\n"
                for teacher_info in teachers_info
            )[:-1]
        )
        self.teacher_label.setWordWrap(True)
        self.teacher_label.setStyleSheet(self.content_stylesheet)

        zoom_text = f"Zoom link: <a href=\"{self.course.zoomLink}\" style=\"color: {{color}}\">{self.course.zoomLink}</a>"
        self.zoom_link_label = QLabel(zoom_text.format(color="white"))
        self.zoom_link_label.linkHovered.connect(
            lambda link, label=self.zoom_link_label, original_text=zoom_text:
            hyperlink_color_change(link, label, original_text, "white", "blue")
        )
        self.zoom_link_label.setTextFormat(Qt.TextFormat.RichText)
        self.zoom_link_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.zoom_link_label.setOpenExternalLinks(True)
        self.zoom_link_label.setStyleSheet(self.content_stylesheet)
        
        classrooms = database.getClassroomsForCourse(self.course.courseCode)
        classrooms = list(dict.fromkeys(classrooms))    #remove duplicates
        self.classroom_label = QLabel(
            "".join(
                f"{classroom}, "
                for classroom in classrooms
            )[:-2]
        )
        self.classroom_label.setWordWrap(True)
        self.classroom_label.setStyleSheet(self.content_stylesheet)

        teacher_msgs = database.getTeacherMessages(self.course.courseCode)
        self.teacher_msgs_label = QLabel(
            "".join(
                f"{teacher_msg[1]}\n\t{teacher_msg[0]}\n\n"
                for teacher_msg in teacher_msgs
            )[:-2]
        )
        self.teacher_msgs_label.setWordWrap(True)
        self.teacher_msgs_label.setStyleSheet(self.content_stylesheet)

        self.group_material_widgets = self.generate_group_materials()

        self.mail_link = self.generate_mail_link()      #generate link to send email to teacher
        self.email_btn = QPushButton("Send to email")
        self.email_btn.setFlat(True)
        self.email_btn.clicked.connect(
            lambda: QDesktopServices.openUrl(self.mail_link)
        )
        self.email_btn.setStyleSheet(self.button_stylesheet)

        self.expand_layout.addWidget(self.description_label)
        self.expand_layout.addWidget(self.teacher_label)
        self.expand_layout.addWidget(self.zoom_link_label)
        self.expand_layout.addWidget(self.classroom_label)
        self.expand_layout.addWidget(self.teacher_msgs_label)
        for group_material_widget in self.group_material_widgets:
            self.expand_layout.addWidget(group_material_widget)
        self.expand_layout.addWidget(self.email_btn)
        self.expand_layout.addStretch(1)

        self.expand_content = QFrame()
        self.expand_content.setLayout(self.expand_layout)

        self.frame_stylesheet = '''
            QFrame {
                background-color: rgba(170, 196, 255, 60%);
                color: white;
                border: 0;
                border-radius: 5px;
                width: 80px;
                padding: 10px;
                font-size: 20px;
            }

            QPushButton {
                background-color: #AAC4FF; 
                border: 2px #B1B2FF;
                border-radius: 5px; 
                border-style: none solid solid none;
                padding: 10px 20px;
                color: #ffffff; 
                font-family: ubuntu, arial; 
                font-size: 20px;
            } 
            
            QPushButton:hover {
                background-color: #C6D0FF;
                border: 0;
            }
        '''
        self.expand_content.setStyleSheet(self.frame_stylesheet)

        self.expand_height = self.expand_content.sizeHint().height()
        self.expand_content.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)
        self.expand_content.setFixedHeight(0)

        self.main_layout.addWidget(self.down_btn)
        self.main_layout.addWidget(self.expand_content)
        self.setLayout(self.main_layout)

    def expand_entity(self):
        self.expand_anim = QVariantAnimation(self)
        self.expand_anim.setDuration(100)
        self.expand_anim.setEasingCurve(QEasingCurve.Type.Linear)
        if (self.expand_content.height() == 0):
            self.expand_anim.setStartValue(self.expand_content.height())
            self.expand_anim.setEndValue(self.expand_height)
            self.down_btn.setIcon(QIcon('assets/chevron_up.png'))
        else:
            self.expand_anim.setStartValue(self.expand_content.height())
            self.expand_anim.setEndValue(0)
            self.down_btn.setIcon(QIcon('assets/chevron_down.png'))
        
        self.expand_anim.valueChanged.connect(
            lambda val: self.expand_content.setFixedHeight(val)
        )
        self.expand_anim.start()

    def generate_group_materials(self) -> 'list[CourseGroupMaterials]':
        self.group_to_materials = {
            group_name: database.getMaterialsForGroup(course.courseCode, group_id)
            for group_id, group_name in database.getMaterialGroupsForCourse(course.courseCode)
        }

        group_material_widgets = []
        for group_name, materials in self.group_to_materials.items():
            if materials is None:
                continue
            group_material_widgets.append(self.CourseGroupMaterials(group_name, materials))
        
        return group_material_widgets
    
    def generate_mail_link(self) -> QUrl:
        return QUrl(
            "mail to:" + database.getStudent(data.student_id) +
            "?subject=" + QUrl.toPercentEncoding("Course Details of " + self.course.courseCode + ": " + self.course.courseName).data().decode() +
            "&body=" + QUrl.toPercentEncoding(self.text()).data().decode(),
            QUrl.ParsingMode.TolerantMode
        )

    def text(self) -> str:
        text = ""
        text += self.title_label.text() + "\n\n"
        text += self.description_label.text() + "\n\n"
        text += self.teacher_label.text() + "\n\n"
        rich_text = self.zoom_link_label.text()
        link = find_between_substrings(rich_text, "<a href=\"", "\">")
        content = find_between_substrings(rich_text, ">", "</a>")
        text += f"name: {content}; link: {link}\n\n"
        text += self.classroom_label.text() + "\n\n"
        text += self.teacher_msgs_label.text() + "\n\n"
        for group_material_widget in self.group_material_widgets:
            text += group_material_widget.text() + "\n"
        
        return text

    class CourseGroupMaterials(QWidget):
        def __init__(self, groupName: str, materials: "list[List[str,str]]"):
            super().__init__()
            self.groupName = groupName
            self.materials = materials
            self.init_UI()

        def init_UI(self):
            self.main_layout = QVBoxLayout()

            title_font = QFont()
            title_font.setBold(True)
            title_font.setPixelSize(40)

            content_stylesheet = '''
                QLabel {
                    font-size: 20px;
                }
            '''

            self.group_name = QLabel(self.group.groupName)
            self.group_name.setWordWrap(True)
            self.group_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.group_name.setFont(title_font)

            self.horizontal_line = QFrame()
            self.horizontal_line.setFrameShape(QFrame.Shape.HLine)
            self.horizontal_line.setFrameShadow(QFrame.Shadow.Sunken)

            self.material_labels: list[QLabel] = []
            idx = 1
            for material in self.materials:
                material_label = QLabel(f"{idx}.&nbsp;<a href=\"{material[0]}\">{material[1]}</a>")
                material_label.setTextFormat(Qt.TextFormat.RichText)
                material_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
                material_label.setOpenExternalLinks(True)
                material_label.setWordWrap(True)
                material_label.setStyleSheet(content_stylesheet)
                self.material_labels.append(material_label)
                idx += 1
            
            self.main_layout.addWidget(self.group_name)
            self.main_layout.addWidget(self.horizontal_line)
            for material_label in self.material_labels:
                self.main_layout.addWidget(material_label)
            
            self.main_layout.addStretch(1)

            self.setLayout(self.main_layout)

        def text(self) -> str:
            text = ""
            text += self.group_name.text() + "\n"
            for material_label in self.material_labels:
                rich_text = material_label.text()
                idx = rich_text[0:1]
                link = find_between_substrings(rich_text, "<a href=\"", "\">")
                content = find_between_substrings(rich_text, ">", "</a>")
                text += f"{idx}. name: {content}; link: {link}\n"

            return text

def find_between_substrings(to_find, left_substring, right_substring):
    from re import search
    try:
        return search(left_substring + "(.+?)" + right_substring, to_find).group(1)
    except Exception:
        return ""

def hyperlink_color_change(link, label: QLabel, original_text: str, original_color: str, hover_color: str):
    if link:
        label.setText(original_text.format(color=hover_color))
        label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    else:
        label.setText(original_text.format(color=original_color))
        label.unsetCursor()