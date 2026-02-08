name: Build Android and Windows
on: [push, workflow_dispatch]

jobs:
  # --- بناء نسخة الأندرويد APK ---
  android-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build APK with Buildozer
        uses: ArtemSerebrenninkov/buildozer-action@v1
        with:
          buildozer_version: master
          command: buildozer android debug
      - name: Upload APK Link
        uses: actions/upload-artifact@v3
        with:
          name: Android-APK-File
          path: bin/*.apk

  # --- بناء نسخة الويندوز EXE ---
  windows-build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install Dependencies
        run: |
          pip install kivy[base] arabic-reshaper python-bidi pyinstaller
      - name: Build EXE
        run: |
          # سيتم إنشاء ملف تشغيلي واحد يضم كل شيء
          pyinstaller --onefile --noconsole --add-data "font.ttf;." main.py
      - name: Upload Windows Link
        uses: actions/upload-artifact@v3
        with:
          name: Windows-EXE-File
          path: dist/*.exe
