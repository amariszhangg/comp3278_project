INSERT INTO
    Student (name, email, face_id)
VALUES
    ('Eddie', 'eddie@gmail.com', 1);

INSERT INTO
    Student (name, email, face_id)
VALUES
    ('Amaris', 'amaris@gmail.com', 2);

INSERT INTO
    Student (name, email, face_id)
VALUES
    ('Angus', 'angus@gmail.com', 3);

INSERT INTO
    Student (name, email, face_id)
VALUES
    ('Jonathan', 'jonathan@gmail.com', 4);

INSERT INTO
    Student (name, email, face_id)
VALUES
    ('Dex', 'dex@gmail.com', 5);

INSERT INTO
    Teacher (name, email)
VALUES
    ('Dr. Ping Luo', 'pluo@cs.hku.hk');

INSERT INTO
    Course (
        course_code,
        teacher_id,
        course_name,
        zoom_link,
        course_description
    )
VALUES
    (
        'COMP3278',
        1,
        'Introduction to Database Management Systems',
        'https://hku.zoom.us/j/98307568693?pwd=QmlqZERWeDdWRVZ3SGdqWG51YUtndz09',
        'Able to understand the modeling of real-life information in a database system.'
    );

INSERT INTO
    Enrolled (student_id, course_code)
VALUES
    (1, 'COMP3278');

INSERT INTO
    Enrolled (student_id, course_code)
VALUES
    (2, 'COMP3278');

INSERT INTO
    LoginRecord (student_id, login_time, logout_time)
VALUES
    (1, '2023-10-02 11:32:42', '2023-10-02 17:24:44');

INSERT INTO
    Schedule (course_code, start_time, end_time, classroom)
VALUES
    (
        'COMP3278',
        '2023-11-02 13:30:00',
        '2023-11-02 15:20:00',
        'MWT1'
    );

INSERT INTO
    Schedule (course_code, start_time, end_time, classroom)
VALUES
    (
        'COMP3278',
        '2023-11-06 14:30:00',
        '2023-11-06 15:20:00',
        'MWT1'
    );

INSERT INTO
    CourseMaterialSection (course_code, group_name)
VALUES
    ('COMP3278', 'Announcement');

INSERT INTO
    CourseMaterialSection (course_code, group_name)
VALUES
    ('COMP3278', 'Assignment');

INSERT INTO
    CourseMaterialSection (course_code, group_name)
VALUES
    ('COMP3278', 'SQL Challenge');

INSERT INTO
    Material (course_code, group_id, material_name, link)
VALUES
    (
        'COMP3278',
        1,
        'News Announcement',
        'https://moodle.hku.hk/mod/forum/view.php?id=2987421'
    );

INSERT INTO
    Material (course_code, group_id, material_name, link)
VALUES
    (
        'COMP3278',
        2,
        'Assignment 1',
        'https://moodle.hku.hk/mod/assign/view.php?id=3097603'
    );

INSERT INTO
    Material (course_code, group_id, material_name, link)
VALUES
    (
        'COMP3278',
        2,
        'Assignment 2',
        'https://moodle.hku.hk/mod/assign/view.php?id=3145076'
    );

INSERT INTO
    TeacherMessage (course_code, message, post_time)
VALUES
    (
        'COMP3278',
        'Welcome to COMP3278!',
        '2023-11-06 14:30:00'
    );