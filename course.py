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


course_widget = QWidget()

course_layout = QVBoxLayout()
course_layout.addStretch(1)

scroll_content = QWidget()
scroll_content.setLayout(course_layout)

scroll_area = QScrollArea()
scroll_area.setWidgetResizable(True)
scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
scroll_area.setWidget(scroll_content)

course_layout.addWidget(scroll_area)

@dataclass
class Course:
    courseCode: str
    teacherId: int
    courseName: str
    zoomLink: str
    courseDescription: str

@dataclass
class Material:
    materialId: int
    courseCode: str
    groupId: int
    materialName: str
    link: str

courses: list[Course] = [
    database.getCourse(course_code)
    for course_code in database.getEnrolled(data.student_id)
    if course_code is not None
    ]

course_code_to_pageindex: dict[str, int] = {}
index = 0
for course in courses:
    CourseEntityWidget_layout = QVBoxLayout()

    down_button = QPushButton(QIcon("assets/chevron_down.png"), f"{course.courseCode}: {course.courseName}")
    down_button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    down_button.setFlat(True)
    button_stylesheet = '''
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
    down_button.setStyleSheet(button_stylesheet)   
    down_button.clicked.connect(expand_entity)      #to be done

    subtitle_stylesheet = '''
    QLabel {
        font-size: 25px;
        font-weight: bold;
    }
    '''

    content_stylesheet = '''
        QLabel {
            font-size: 20px;
            padding-left: 30px;
            margin-bottom: 20px;
        }
    '''
    
    expand_layout = QVBoxLayout()

    description_title_label = QLabel("Course Description:")
    description_title_label.setStyleSheet(subtitle_stylesheet)
    description_label = QLabel(f"{course.courseDescription}")
    description_label.setWordWrap(True)
    description_label.setStyleSheet(content_stylesheet)
    description_label.adjustSize()

    teacher_title_label = QLabel("Teacher:")
    teacher_title_label.setStyleSheet(subtitle_stylesheet)
    teachers = [database.getTeachersForCourse(course.courseCode)]
    teacher_label = QLabel(
        "Teacher:" + 
        "".join(
            f"\n\tName: {teacher[0]}\n\tEmail: {teacher[1]}\n"
            for teacher in teachers
        )[:-1]
    )
    teacher_label.setWordWrap(True)
    teacher_label.setStyleSheet(content_stylesheet)

    zoom_title_label = QLabel("Zoom link:")
    zoom_title_label.setStyleSheet(subtitle_stylesheet)
    zoom_text = f"Zoom link: <a href=\"{course.zoomLink}\" style=\"color: {{color}}\">{course.zoomLink}</a>"
    zoom_label = QLabel(zoom_text.format(color="white"))
    zoom_label.linkHovered.connect(
        lambda link, label= zoom_label, original_text=zoom_text:
        text_colour(link, label, original_text, "white", "blue")
    )
    zoom_label.setTextFormat(Qt.TextFormat.RichText)
    zoom_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
    zoom_label.setOpenExternalLinks(True)
    zoom_label.setStyleSheet(content_stylesheet)

    classroom_title_label = QLabel("Classroom address:")
    classroom_title_label.setStyleSheet(subtitle_stylesheet)
    classrooms = database.getClassroomsForCourse(course.courseCode)
    classrooms = list(dict.fromkeys(classrooms)) # remove duplicates
    classroom_label = QLabel(
        "".join(
            f"{classroom}, "
            for classroom in classrooms
        )[:-2]
    )
    classroom_label.setWordWrap(True)
    classroom_label.setStyleSheet(content_stylesheet)

    teacher_msgs_title_label = QLabel("Teacher's messages:")
    teacher_msgs_title_label.setStyleSheet(subtitle_stylesheet)
    teacher_msgs = database.getTeacherMessages(course.courseCode)
    teacher_msgs_label = QLabel(
        "".join(
            f"{teacher_msg[1]}\n\t{teacher_msg[0]}\n\n"
            for teacher_msg in teacher_msgs
        )[:-2]
    )
    teacher_msgs_label.setWordWrap(True)
    teacher_msgs_label.setStyleSheet(content_stylesheet)

    #prepare for maaterials widgets
    group_to_materials = {
        group_name: database.getMaterialsForGroup(course.courseCode, group_id)
        for group_id, group_name in database.getMaterialGroupsForCourse(course.courseCode)
    }

    # mail_link = 
    # email_button = QPushButton("Send to email")
    # email_button.setFlat(True)
    # email_button.clicked.connect(
    #     lambda: QDesktopServices.openUrl(mail_link)
    # )
    # email_button.setStyleSheet(button_stylesheet)

    expand_layout.addWidget(description_title_label)
    expand_layout.addWidget(description_label)
    expand_layout.addWidget(teacher_title_label)
    expand_layout.addWidget(teacher_label)
    expand_layout.addWidget(zoom_title_label)
    expand_layout.addWidget(zoom_label)
    expand_layout.addWidget(classroom_title_label)
    expand_layout.addWidget(classroom_label)
    expand_layout.addWidget(teacher_msgs_title_label)
    expand_layout.addWidget(teacher_msgs_label)
    
    #add material widgets according to group
    for group, materials in group_to_materials.items():
        material_layout = QVBoxLayout()
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPixelSize(40)

        materials_group_title_label = QLabel(group)
        materials_group_title_label.setWordWrap(True)
        materials_group_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        materials_group_title_label.setFont(title_font)

        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.Shape.HLine)
        horizontal_line.setFrameShadow(QFrame.Shadow.Sunken)

        material_labels: list[QLabel] = []
        idx = 1
        for material in materials:
            material_label = QLabel(f"{idx}.&nbsp;<a href=\"{material[0]}\">{material[1]}</a>")
            material_label.setTextFormat(Qt.TextFormat.RichText)
            material_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
            material_label.setOpenExternalLinks(True)
            material_label.setWordWrap(True)
            material_label.setStyleSheet(content_stylesheet)
            material_labels.append(material_label)
            idx += 1
        
        material_layout.addWidget(materials_group_title_label)
        material_layout.addWidget(horizontal_line)
        for material_label in material_labels:
            material_layout.addWidget(material_label)
        
        material_layout.addStretch(1)
        expand_layout.setLayout(material_layout)

    expand_layout.addStretch(1)

    expand_content = QFrame()
    expand_content.setLayout(expand_layout)

    frame_stylesheet = '''
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
    expand_content.setStyleSheet(frame_stylesheet)

    expand_height = expand_content.sizeHint().height()
    expand_content.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)
    expand_content.setFixedHeight(0)

    CourseEntityWidget_layout.addWidget(down_button)
    CourseEntityWidget_layout.addWidget(expand_content)
    course_layout.addWidget(CourseEntityWidget_layout)


#display all course, click cource show course description teachers, zoom link, class address, teacher message

#function to change text colour
def text_colour(link, label: QLabel, original_text: str, original_color: str, hover_color: str):
    if link:
        label.setText(original_text.format(color=hover_color))
        label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    else:
        label.setText(original_text.format(color=original_color))
        label.unsetCursor()
