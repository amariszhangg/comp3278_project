# comp3278_project

intelligent course management system

## Installation

```bash
pip install -r requirements.txt
```

## Getting Started

1. Copy `.env.example` as `.env`, fill in the necessary environment variables.

2. Create tables using the sql file `database/create_tables2.sql` and insert dummy values with `database/dummy_data2.sql`

3. Capture some photo for face recognition

```bash
cd FaceRecognition
python face_capture.py
```

4. Train the model

```bash
python train.py
```

5. Run the main program

## TODO

we need:

1. login page
2. main GUI after logging in that shows the class in the next hour OR a personal timetable (maybe a logout button)
3. table schema, maybe an ER diagram and tables
4. ppt slides
5. video demo
