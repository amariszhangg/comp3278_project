# comp3278_project

intelligent course management system

## Installation

```bash
pip install -r requirements.txt
```

#both VScode and local

## Getting Started

1. Rename `.env.example` as `.env`, amend the name, add data/Angus under FaceRecognition, select more photos for face_capture.py

2. Create tables using the sql file `database/create_tables2.sql` and insert dummy values with `database/dummy_data2.sql`
   MySQL Workbench

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

```bash
python main.py
```

## TODO

Internal DDL, 15/11:

1. improved UI for login (Dex)
2. merged login and GUI (Jonathan)
3. functions to call data (Angus)

Final DDL, 22/11, we need:

1. login page
2. course page
3. home page
4. schedule page
5. table schema, maybe an ER diagram and tables
6. ppt slides (3 pages, cheat by including layers)
   https://docs.google.com/presentation/d/1Yf7OuEdqYgQwmQ74nxbXVPyFcyTXsXSYJoHCzis7Tsw/edit?usp=sharing
   4.1 design features (showcase interfaces)
   4.2 database implementation and design
   4.3 final entities and design
   4.4 Problems faced and addressed
7. video demo
