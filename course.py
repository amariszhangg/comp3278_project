from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QMainWindow, QMessageBox, QLabel
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QScrollArea, QSizePolicy
from PyQt5.QtGui import QIcon, QFont, QDesktopServices, QCursor
from PyQt5.QtCore import Qt, QVariantAnimation, QEasingCurve, QUrl, QSize

import database
import data
from typing import List

import datetime
from dataclasses import dataclass

def hyperlink_color_change(link, label: QLabel, original_text: str, original_color: str, hover_color: str):
    if link:
        label.setText(original_text.format(color=hover_color))
        label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    else:
        label.setText(original_text.format(color=original_color))
        label.unsetCursor()

def find_between_substrings(to_find, left_substring, right_substring):
    from re import search
    try:
        return search(left_substring + "(.+?)" + right_substring, to_find).group(1)
    except Exception:
        return ""

def create_course_widget(course):
    course_entity_widget = QWidget()
    course_entity_layout = QVBoxLayout()
    course_entity_layout.setAlignment(Qt.AlignCenter)

    down_button = QPushButton(QIcon("assets/chevron_down.png"), f"{course.courseCode}: {course.courseName}")
    down_button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    down_button.setFlat(True)
    button_stylesheet = '''
        QPushButton {
            background-color: #4AA080; 
            border: 2px #B1B2FF;
            border-radius: 2px; 
            border-style: none solid solid none;
            padding: 5px 10px;
            color: #ffffff; 
            font-family: Arial, sans-serif; 
            font-size: 18px;
        } 
        
        QPushButton:hover {
            background-color: #34AD81;
            border: 0;
        }
    '''
    down_button.setStyleSheet(button_stylesheet)  

    expand_layout = QVBoxLayout()

    content_stylesheet = '''
        QLabel {
            font-size: 14px;
            padding-left: 5px;
            margin-bottom: 1px;
        }
    '''

    description_label = QLabel(f"Course Description:\n{course.courseDescription}")
    description_label.setWordWrap(True)
    description_label.setStyleSheet(content_stylesheet)
    description_label.adjustSize()

    teachers_info = database.getTeachersForCourse(course.courseCode)
    teacher_label = QLabel(
        "Teacher information:" + 
        "".join(
            f"\nName: {teacher_info[0]}\nEmail: {teacher_info[1]}\n"
            for teacher_info in teachers_info
        )[:-1]
    )
    teacher_label.setWordWrap(True)
    teacher_label.setStyleSheet(content_stylesheet)

    zoom_text = f"Zoom link: <a href=\"{course.zoomLink}\" style=\"color: {{color}}\">{course.zoomLink}</a>"
    zoom_link_label = QLabel(zoom_text.format(color="white"))
    zoom_link_label.linkHovered.connect(
        lambda link, label=zoom_link_label, original_text=zoom_text:
        hyperlink_color_change(link, label, original_text, "white", "blue")
    )
    zoom_link_label.setTextFormat(Qt.TextFormat.RichText)
    zoom_link_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
    zoom_link_label.setOpenExternalLinks(True)
    zoom_link_label.setStyleSheet(content_stylesheet)

    classrooms = database.getClassroomsForCourse(course.courseCode)
    classrooms = list(dict.fromkeys(classrooms))    #remove duplicates
    classroom_label = QLabel(
        "Classroom(s): " + 
        "".join(
            f"{classroom}, "
            for classroom in classrooms
        )[:-2]
    )
    classroom_label.setWordWrap(True)
    classroom_label.setStyleSheet(content_stylesheet)

    teacher_msgs = database.getTeacherMessages(course.courseCode)
    teacher_msgs_label = QLabel(
        "Teacher Messages:\n" + 
        "".join(
            f"{teacher_msg[1]}\n{teacher_msg[0]}\n\n"
            for teacher_msg in teacher_msgs
        )[:-2]
    )
    teacher_msgs_label.setWordWrap(True)
    teacher_msgs_label.setStyleSheet(content_stylesheet)

    group_to_materials = {}
    for group_id, group_name in database.getMaterialGroupsForCourse(course.courseCode):
        if database.getMaterialsForGroup(course.courseCode, group_id) != None:
            group_to_materials[group_name] = database.getMaterialsForGroup(course.courseCode, group_id)
    
    def selftext():
        text = ""
        text += description_label.text() + "\n\n"
        text += teacher_label.text() + "\n\n"
        rich_text = zoom_link_label.text()
        link = find_between_substrings(rich_text, "<a href=\"", "\">")
        content = find_between_substrings(rich_text, ">", "</a>")
        text += f"name: {content}; link: {link}\n\n"
        text += classroom_label.text() + "\n\n"
        text += teacher_msgs_label.text() + "\n\n"
        for group, materials in group_to_materials.items():     #loop through different groups of materials
            text += group + "\n"
            idx = 1
            for material in materials:
                material_label = QLabel(f"{idx}.&nbsp;<a href=\"{material[0]}\">{material[1]}</a>")
                rich_text = material_label.text()
                idx = rich_text[0:1]
                link = find_between_substrings(rich_text, "<a href=\"", "\">")
                content = find_between_substrings(rich_text, ">", "</a>")
                text += f"{idx}. name: {content}; link: {link}\n"
                text += "\n"
        return text

    text = selftext()
    mail_to_link = QUrl(
        "mail to:" + database.getStudent(3)[2] +
        "?subject=" + QUrl.toPercentEncoding("Course Details of " + course.courseCode + ": " + course.courseName).data().decode() +
        "&body=" + QUrl.toPercentEncoding(text).data().decode(),
        QUrl.ParsingMode.TolerantMode
    )
    email_button = QPushButton("Send to email")
    email_button.setFlat(True)
    email_button.clicked.connect(
        lambda: QDesktopServices.openUrl(mail_to_link)
    )
    email_button.setStyleSheet(content_stylesheet)

    expand_layout.addWidget(description_label)
    expand_layout.addWidget(teacher_label)
    expand_layout.addWidget(zoom_link_label)
    expand_layout.addWidget(classroom_label)
    expand_layout.addWidget(teacher_msgs_label)
    for group, materials in group_to_materials.items():     #expand_layout.addWidgets(materialss)
        group_label = QLabel(group+':\n')
        group_label.setWordWrap(True)
        group_label.setStyleSheet(content_stylesheet)
        expand_layout.addWidget(group_label)
        idx = 1
        for material in materials:
            material_label = QLabel(f"{idx}.&nbsp;<a href=\"{material[0]}\">{material[1]}</a>")
            material_label.setTextFormat(Qt.TextFormat.RichText)
            material_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
            material_label.setOpenExternalLinks(True)
            material_label.setStyleSheet(content_stylesheet)
            idx += 1
            expand_layout.addWidget(material_label)
    expand_layout.addWidget(email_button)

    expand_content = QFrame()
    expand_content.setLayout(expand_layout)

    frame_stylesheet = '''
        QFrame {
            background-color: #4AA080;
            color: white;
            border: 0;
            border-radius: 2px;
            width: 80px;
            padding: 5px;
            font-size: 12px;
        }

        QPushButton {
            background-color: #4AA080; 
            border: 2px #B1B2FF;
            border-radius: 2px; 
            border-style: none solid solid none;
            padding: 5px 10px;
            color: #ffffff; 
            font-family: ubuntu, arial; 
            font-size: 12px;
        } 
        
        QPushButton:hover {
            background-color: #34AD81;
            border: 0;
        }
    '''
    expand_content.setStyleSheet(frame_stylesheet)

    scroll_content = QWidget()
    scroll_content.setLayout(course_entity_layout)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll_area.setWidget(scroll_content)

    wrap_layout = QVBoxLayout()
    wrap_layout.addWidget(scroll_area)
    course_entity_widget.setLayout(wrap_layout)

    expand_height = expand_content.sizeHint().height()
    expand_content.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)
    expand_content.setFixedHeight(0)

    expand_anim = QVariantAnimation()
    expand_anim.setDuration(100)
    expand_anim.setEasingCurve(QEasingCurve.Type.Linear)

    def update_animation():
        if expand_content.height() == 0:
            expand_anim.setStartValue(expand_content.height())
            expand_anim.setEndValue(expand_height)
            down_button.setIcon(QIcon('assets/chevron_up.png'))
        else:
            expand_anim.setStartValue(expand_content.height())
            expand_anim.setEndValue(0)
            down_button.setIcon(QIcon('assets/chevron_down.png'))
        expand_anim.start()

    def update_animation_on_click():
        update_animation()
        expand_content.setFixedHeight(expand_anim.currentValue())

    down_button.clicked.connect(update_animation_on_click)
    expand_anim.valueChanged.connect(expand_content.setFixedHeight)

    course_entity_layout.addWidget(down_button)
    course_entity_layout.addWidget(expand_content)
    course_entity_widget.setLayout(course_entity_layout)

    return course_entity_widget

@dataclass
class Course:
    courseCode: str
    teacherId: int
    courseName: str
    zoomLink: str
    courseDescription: str

course_widget = QWidget()

course_layout = QVBoxLayout()
course_layout.setAlignment(Qt.AlignCenter)

course_widget.setLayout(course_layout)

courses: List[Course] = []
for student_id, course_code in database.getEnrolled(data.student_id):
    if course_code is not None:
        course_data = database.getCourse(course_code)
        course = Course(
            courseCode=course_data[0],
            teacherId=course_data[1],
            courseName=course_data[2],
            zoomLink=course_data[3],
            courseDescription=course_data[4]
        )
        courses.append(course)

for course in courses:
    course_entity_widget = create_course_widget(course)
    course_layout.addWidget(course_entity_widget)

main_scroll_content = QWidget()
main_scroll_content.setLayout(course_layout)

main_scroll_area = QScrollArea()
main_scroll_area.setWidgetResizable(True)
main_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
main_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
main_scroll_area.setWidget(main_scroll_content)

main_wrap_layout = QVBoxLayout()
main_wrap_layout.addWidget(main_scroll_area)
course_widget.setLayout(main_wrap_layout)





# def update_course_content():
#     for course_code in database.getEnrolled(data.student_id):
#         if course_code is not None:
#             course_data = database.getCourse(course_code)
#             course = Course(
#                 courseCode=course_data[0],
#                 teacherId=course_data[1],
#                 courseName=course_data[2],
#                 zoomLink=course_data[3],
#                 courseDescription=course_data[4]
#             )
#             courses.append(course)

# course_widget = QWidget()

# course_layout = QVBoxLayout()
# course_layout.addStretch(1)

# scroll_content = QWidget()
# scroll_content.setLayout(course_layout)

# scroll_area = QScrollArea()
# scroll_area.setWidgetResizable(True)
# scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
# scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
# scroll_area.setWidget(scroll_content)

# course_layout.addWidget(scroll_area)


# @dataclass
# class Material:
#     materialId: int
#     courseCode: str
#     groupId: int
#     materialName: str
#     link: str


# course_code_to_pageindex: dict[str, int] = {}
# index = 0
# for course in courses:
#     CourseEntityWidget_layout = QVBoxLayout()
 
#     down_button.clicked.connect(expand_entity)      #to be done

#     subtitle_stylesheet = '''
#     QLabel {
#         font-size: 25px;
#         font-weight: bold;
#     }
#     '''

    
#     expand_layout = QVBoxLayout()

#     description_title_label = QLabel("Course Description:")
#     description_title_label.setStyleSheet(subtitle_stylesheet)
#     description_label = QLabel(f"{course.courseDescription}")
#     description_label.setWordWrap(True)
#     description_label.setStyleSheet(content_stylesheet)
#     description_label.adjustSize()

#     teacher_title_label = QLabel("Teacher:")
#     teacher_title_label.setStyleSheet(subtitle_stylesheet)
#     teachers = [database.getTeachersForCourse(course.courseCode)]
#     teacher_label = QLabel(
#         "Teacher:" + 
#         "".join(
#             f"\n\tName: {teacher[0]}\n\tEmail: {teacher[1]}\n"
#             for teacher in teachers
#         )[:-1]
#     )
#     teacher_label.setWordWrap(True)
#     teacher_label.setStyleSheet(content_stylesheet)

#     zoom_title_label = QLabel("Zoom link:")
#     zoom_title_label.setStyleSheet(subtitle_stylesheet)
#     zoom_text = f"Zoom link: <a href=\"{course.zoomLink}\" style=\"color: {{color}}\">{course.zoomLink}</a>"
#     zoom_label = QLabel(zoom_text.format(color="white"))
#     zoom_label.linkHovered.connect(
#         lambda link, label= zoom_label, original_text=zoom_text:
#         text_colour(link, label, original_text, "white", "blue")
#     )
#     zoom_label.setTextFormat(Qt.TextFormat.RichText)
#     zoom_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
#     zoom_label.setOpenExternalLinks(True)
#     zoom_label.setStyleSheet(content_stylesheet)

#     classroom_title_label = QLabel("Classroom address:")
#     classroom_title_label.setStyleSheet(subtitle_stylesheet)
#     classrooms = database.getClassroomsForCourse(course.courseCode)
#     classrooms = list(dict.fromkeys(classrooms)) # remove duplicates
#     classroom_label = QLabel(
#         "".join(
#             f"{classroom}, "
#             for classroom in classrooms
#         )[:-2]
#     )
#     classroom_label.setWordWrap(True)
#     classroom_label.setStyleSheet(content_stylesheet)

#     teacher_msgs_title_label = QLabel("Teacher's messages:")
#     teacher_msgs_title_label.setStyleSheet(subtitle_stylesheet)
#     teacher_msgs = database.getTeacherMessages(course.courseCode)
#     teacher_msgs_label = QLabel(
#         "".join(
#             f"{teacher_msg[1]}\n\t{teacher_msg[0]}\n\n"
#             for teacher_msg in teacher_msgs
#         )[:-2]
#     )
#     teacher_msgs_label.setWordWrap(True)
#     teacher_msgs_label.setStyleSheet(content_stylesheet)

#     #prepare for maaterials widgets
#     group_to_materials = {
#         group_name: database.getMaterialsForGroup(course.courseCode, group_id)
#         for group_id, group_name in database.getMaterialGroupsForCourse(course.courseCode)
#     }

#     # mail_link = 
#     # email_button = QPushButton("Send to email")
#     # email_button.setFlat(True)
#     # email_button.clicked.connect(
#     #     lambda: QDesktopServices.openUrl(mail_link)
#     # )
#     # email_button.setStyleSheet(button_stylesheet)

#     expand_layout.addWidget(description_title_label)
#     expand_layout.addWidget(description_label)
#     expand_layout.addWidget(teacher_title_label)
#     expand_layout.addWidget(teacher_label)
#     expand_layout.addWidget(zoom_title_label)
#     expand_layout.addWidget(zoom_label)
#     expand_layout.addWidget(classroom_title_label)
#     expand_layout.addWidget(classroom_label)
#     expand_layout.addWidget(teacher_msgs_title_label)
#     expand_layout.addWidget(teacher_msgs_label)
    
#     #add material widgets according to group
#     for group, materials in group_to_materials.items():
#         material_layout = QVBoxLayout()
#         title_font = QFont()
#         title_font.setBold(True)
#         title_font.setPixelSize(40)

#         materials_group_title_label = QLabel(group)
#         materials_group_title_label.setWordWrap(True)
#         materials_group_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         materials_group_title_label.setFont(title_font)

#         horizontal_line = QFrame()
#         horizontal_line.setFrameShape(QFrame.Shape.HLine)
#         horizontal_line.setFrameShadow(QFrame.Shadow.Sunken)

#         material_labels: list[QLabel] = []
#         idx = 1
#         for material in materials:
#             material_label = QLabel(f"{idx}.&nbsp;<a href=\"{material[0]}\">{material[1]}</a>")
#             material_label.setTextFormat(Qt.TextFormat.RichText)
#             material_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
#             material_label.setOpenExternalLinks(True)
#             material_label.setWordWrap(True)
#             material_label.setStyleSheet(content_stylesheet)
#             material_labels.append(material_label)
#             idx += 1
        
#         material_layout.addWidget(materials_group_title_label)
#         material_layout.addWidget(horizontal_line)
#         for material_label in material_labels:
#             material_layout.addWidget(material_label)
        
#         material_layout.addStretch(1)
#         expand_layout.setLayout(material_layout)

#     expand_layout.addStretch(1)

#     expand_content = QFrame()
#     expand_content.setLayout(expand_layout)

#     frame_stylesheet = '''
#         QFrame {
#             background-color: rgba(170, 196, 255, 60%);
#             color: white;
#             border: 0;
#             border-radius: 5px;
#             width: 80px;
#             padding: 10px;
#             font-size: 20px;
#         }

#         QPushButton {
#             background-color: #AAC4FF; 
#             border: 2px #B1B2FF;
#             border-radius: 5px; 
#             border-style: none solid solid none;
#             padding: 10px 20px;
#             color: #ffffff; 
#             font-family: ubuntu, arial; 
#             font-size: 20px;
#         } 
        
#         QPushButton:hover {
#             background-color: #C6D0FF;
#             border: 0;
#         }
#     '''
#     expand_content.setStyleSheet(frame_stylesheet)

#     expand_height = expand_content.sizeHint().height()
#     expand_content.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)
#     expand_content.setFixedHeight(0)

#     CourseEntityWidget_layout.addWidget(down_button)
#     CourseEntityWidget_layout.addWidget(expand_content)
#     course_layout.addWidget(CourseEntityWidget_layout)


# #display all course, click cource show course description teachers, zoom link, class address, teacher message

# #function to change text colour
# def text_colour(link, label: QLabel, original_text: str, original_color: str, hover_color: str):
#     if link:
#         label.setText(original_text.format(color=hover_color))
#         label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
#     else:
#         label.setText(original_text.format(color=original_color))
#         label.unsetCursor()
