# TabletTalk Patch - linux version
These are the steps I followed to patch my Tablet Talk APK to work on android 7.0

I basically adapted the work from https://github.com/freshollie/TabletTalkLollipopPatch but changed the method that actually answers the call as the solution was not working for my Samsung S6 edge+ (Nougat).

Why
---

In android 5.0 google changed the way answering the phone works.

Tablet Talk is an app that allows you to answer the phone from a tablet, and has not been updated properly since 4.4.

Without patching the APK the tablet talk app will just not answer. The problem is in the code in the phone. Proper API for programmatically answering incoming phone calls exists only for Android 8 (Oreo) and newer (see https://stackoverflow.com/a/29651130/8179862).

This source code will allow you to patch your own APK (for your phone) to answer incoming calls.

Requirements
------------
- java in your system path
- your phone must be rooted to be able to run scripts as superuser
- zipalign at your pc (For linux mint just sudo apt-get install zipalign)
- Install 7za and optipng at your pc (if you decide to uncomment the image optimization in the buildapk script, but you must also edit the code to recursively optimize images)

The actual steps that worked for me:
-----

- Download this source code.
The important code is in directory “assets”. However, file “ServicePhone.smali” is from a version of Tablet Talk that may not be the same as yours. It must be replaced with the version found after decoding the original Tablet Talk apk, and then edited to instantiate activity AcceptCall which does the actual call answering.

- Once you buy and install the official Tablet Talk apk from Goggle PlayStore in your phone, use a program such as “Apk Extractor” to extract the apk.

- Copy the extracted apk of the official Tablet Talk app in the folder where you downloaded the source code from here.

- In a terminal window run `java -jar -Duser.language=en apktool.jar -f d #TabletTalk.apk#` replacing #TabletTalk.apk# with the actual name of the apk that was extracted from the original application in the phone.
    - The first time time that the apktool runs, it will save file “1.apk” in /home/$USER/apktool/framework. This file is not guaranteed to be appropriate for you phone. I deleted /home/$USER/apktool/framework/1.apk and for my Samsung S6 edge+ I copied the samsung framework apk from my phone using `adb shell system/framework/framework-res.apk` and installed it at my pc running `java -jar -Duser.language=en apktool.jar if framework-res.apk`.

- The lines that must be added in the original ServicePhone.smali file should be added at the end of function `.method protected final d()V`
```
    new-instance v0, Landroid/content/Intent;
    const-class v1, Lcom/apdroid/tabtalk/AcceptCallActivity;
    invoke-direct {v0, p0, v1}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .local v0, "intent":Landroid/content/Intent;
    const v1, 0x10808000

    invoke-virtual {v0, v1}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;

    invoke-virtual {p0, v0}, Landroid/content/Context;->startActivity(Landroid/content/Intent;)V
```

- Also, the method used in AcceptCallActivity.smali for answering the call will not work (not for Nougat anyway). Instead the only method I found working, is running an su script that will call the phone service to answer the call. See http://bamboopuppy.com/making-an-android-shell-script/, http://su.chainfire.eu/#how and https://stackoverflow.com/a/25987388/8179862

    Add the following lines at the beginning of method  `.method private acceptCall()V`

```
    :try_start_ahat_0
    const-string v0, "su -c /data/answer_call"
    invoke-static {}, Ljava/lang/Runtime;->getRuntime()Ljava/lang/Runtime;
    move-result-object v1
    invoke-virtual {v1, v0}, Ljava/lang/Runtime;->exec(Ljava/lang/String;)Ljava/lang/Process;
    :try_end_ahat_0
    .catchall {:try_start_ahat_0 .. :try_end_ahat_0} :catchall_ahat

    return-void

    :catchall_ahat
    move-exception v2
    throw v2
```

- At your pc (with the phone connected with a usb cable) run `adb shell` in a terminal.
    - Once you are in the adb shell run `su` (the SuperUser app must be installed in your phone), and in the dialog that pops up in your phone grant superuser permission to application adb.
    - In the adb shell run the following command `echo “service call phone #n#” > /data/answer_call`
        - Replace #n# with the appropriate code number that will answer incoming calls. For Nougat this seems to be 7. In previous Android versions this was 5 or 6. I found out by calling my phone from another phone and running at my pc `adb shell service call phone x` trying all integers for x from 1 up to 7. 7 did the trick.
        - This creates a script file in /data (if you try /sdcard instead you will find out that sdcard is mounted without the execute permission and therefore answer_call cannot become executable -chmod +x will do nothing-).
    - In the adb shell run `chmod +x /data/answer_call` to make answer_call executable. Test by calling from another and try to answer the call by running in the adb shell `sh /data/answer_call`.

- Run script patch to generate a patched apk for Tablet Talk

- Copy the patched apk to you phone.

- Uninstall the original Tablet Talk app that you install from the Google Playstore

- Install the patched apk in your phone (open a file manager, go to the dir where you copied the patched apk and double click it).

- Install the original Tablet Talk apk (from Google Playstore, or rather from library since you have alrady paid for it when you first bought it and installed it in your phone) in your tablet, no patching is required here!

- Run the Tablet Talk apps (original in tablet, patched in phone) and establish a connection between the two.

- Call your phone from another phone and answer from your tablet.
    - You will **NOT** be able to answer the call because you have not granted superuser permissions to your phone’s Tablet Talk app yet. A toast will notify you about this saying “permission denied etc.”
    - In you phone, find the superuser app, and run it. In the list of applications you should see Tablet Talk. Click it and grant it superuser permissions. Now Tablet Talk can run the answer call script as superuser.

- Call again your phone from another phone and answer from your tablet. Now you **CAN** answer the call.

Notes:
------
I adapted the patch and buildapk scripts for linux. I chose not to optimize the images because it seemed too much of a pain for little gain.

In case of crashes or other error one way to see what is going on is to run `adb logcat AndroidRuntime:E *:S` at your pc while your phone is connected over usb and run Tablet Talk.

Dalvik opcodes to find out what each smali command does http://pallergabor.uw.hu/androidblog/dalvik_opcodes.html
