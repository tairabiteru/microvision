# Microvision
 A computer vision program which presses hotkeys based on face detection.

 This program was originally developed to solve a simple problem I had. I have two microphones, a nice one, and one on my headset. When I'm at my computer, I want to use the nice one, but when I'm not, I want to switch to the headset. Programs exist which allow you to bind hotkeys to a microphone pretty easily, like [Audio Switcher](https://audioswit.ch/er). Indeed, this program relies on it ultimately, but the problem with such programs is that I have to remember to push the buttons. This inevitably results in me walking away from my desk as my friends tell me my voice is getting quieter before they hear some four letter words shouted from across the house, followed by me scrambling back to my desk.

 I could instead opt to just remember to push the buttons, but
 
 1. I've been doing this for years and still don't remember, and
 2. I don't want to have to *remember* things, ew!

 Hence, this program. All it does it capture a frame from your computer's camera, then figure out if there's a face in frame. If there is, it presses a configurable hotkey combination. If it does not, it presses a different configurable hotkey combination. Sync that up with [Audio Switcher](https://audioswit.ch/er), and now you have a system which automagically switches your computer's microphone based on face detection.

 ## Limitations
 * This only really works in situations where you're alone. If you can't find a position where you're going to be the only one visible by the camera, this doesn't work for you. The program is doing face *detection*, not face *recognition*. It has no concept of who you are or what you look like. It only knows that you have a face, and if there is a face - any face - it should do something.

 ## FAQ
 * **My camera is always on when using this program. Why?** Simply put, because it is constantly being used by the program. This program needs the camera to perform computer vision tasks on frames it retrieves from it. This behavior is *expected*. 
 * **Will it steal pictures of me?** No. If you're paranoid about it, you can read the source code. There's absolutely no network communication going on, and this program works whether your computer is online or not. If you still don't trust it, perhaps this isn't the program for you.
* **Does this only work with microphones?** Though it was originally designed with microphones in mind, it doesn't really have to work exclusively with them. The program doesn't switch microphones, it sends a key combination. It just so happens in my case that the key combination it sends has been bound in [Audio Switcher](https://audioswit.ch/er) to switch microphones. So if you use another program to make those key combinations do something else, in theory the program could control just about anything.
* **Wow, this is really over engineered. Is it really so hard to push buttons?** It's not really about laziness, more a problem of memory if I'm honest. Also:
![image](https://i.pinimg.com/originals/70/ff/69/70ff693a41dd29b71da8549d1a6a8d5f.png "I can do what I want")

