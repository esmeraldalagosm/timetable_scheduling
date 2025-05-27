# 🕒 Schedule Generator

A Python tool that generates all possible non-overlapping course schedules based on a list of desired classes and available sections.

## 📋 Description

This project helps students generate valid class schedules by reading a CSV file with class data and returning all combinations of sections (one per subject) that do not overlap in time.

## Consider

This was designed base don Universidad Torcuato Di Tella's timetable designed (fixed timeslots shared between all classes).


## 🔧 How It Works

1. You provide:
   - A CSV file with the following columns: `Materia`, `Sección`, `Día`, `Timeslot`, `Tipo`
   - A list of classes you want to enroll in

2. The script:
   - Loads and groups the sections by subject
   - Uses `itertools.product()` to generate all combinations with one section per subject
   - Filters out combinations with overlapping time slots

3. It prints or returns all valid schedules.
4. Tkinter interface: use python3 to run. Limited to 6 subjects due to color assignation (can be easily extended)

