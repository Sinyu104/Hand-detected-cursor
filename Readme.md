## Environment Required
- pynut     1.7.3
- mediapipe 0.8.6.2
- OpenCV 3.x to 4.1 are preferred
- Python 3

## How to run the code?
There are two version of code to run for the hand-detected cursor. The first one is the run the code without Thread, while the other is the one using Threading Method. 
```
git clone https://github.com/Sinyu104/Hand-detected-cursor.git
cd AI_virtual_mouse
python HandTrackingModule.py #to run the handtracking module without threading
python ThreadAiVirtualMouse.py # run the handtracking module with threading
```

## The performance
- Without Thead:
    The FPS is about 30. 
- Use one thread in getting picture:
    The FPS for showing picture is 7~10. 