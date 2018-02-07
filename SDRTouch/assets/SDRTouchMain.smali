.class public Lmarto/androsdr2/SDRTouchMain;
.super Lmarto/sdr/javasdr/SDRRadioActivity;
.source "SDRTouchMain.java"

# interfaces
.implements Landroid/view/View$OnClickListener;
.implements Lmarto/tools/gui/dialogs/DialogFreqChooser$OnFrequencyEnteredCallback;
.implements Lmarto/tools/gui/dialogs/DialogSettings$OnSettingChanged;


# static fields
.field public static final ACTION_SDR_DEVICE_ATTACHED:Ljava/lang/String; = "com.sdrtouch.rtlsdr.SDR_DEVICE_ATTACHED"

.field private static final DEFAULT_LOCALE:Ljava/util/Locale;

.field private static final DIALOG_FREQ_CENT_FREQ:I = 0x0

.field private static final DIALOG_FREQ_OFFSET:I = 0x1

.field private static final DIALOG_ITEMCHOOSER_CATBUTTON:I = 0x2

.field private static final DIALOG_ITEMCHOOSER_MODULATION:I = 0x1

.field private static final DIALOG_ITEMCHOOSER_OPEN:I = 0x4

.field private static final DIALOG_ITEMCHOOSER_PRESET:I = 0x3

.field private static final DIALOG_ITEMCHOOSER_RECORD:I = 0x5

.field private static final DIALOG_STRING_INPUT_ADD_CATEGORY:I = 0x2

.field private static final DIALOG_STRING_INPUT_ADD_PRESET:I = 0x1

.field private static final DIALOG_STRING_INPUT_REMOTE_START:I = 0x5

.field private static final DIALOG_STRING_INPUT_RENAME_CATEGORY:I = 0x4

.field private static final DIALOG_STRING_INPUT_RENAME_PRESET:I = 0x3

.field private static final DIALOG_YESNO_APP_STORE_MOVED:I = 0x5

.field private static final DIALOG_YESNO_DELETE_CAT:I = 0x1

.field private static final DIALOG_YESNO_DELETE_PRESET:I = 0x2

.field private static final DIALOG_YESNO_OVERRIDE_EXPORT:I = 0x3

.field private static final DIALOG_YESNO_UNSAFE_IMPORT:I = 0x4

.field private static final EXPORT_FILENAME:Ljava/lang/String; = "SDRTouchPresets.xml"

.field private static final FREQ_COMPARATOR_ACCURACY_WITHIN:J = 0x3e8L

.field public static final PREFS_NAME:Ljava/lang/String; = "SDRTouchMain"

.field public static final PREF_CAT:Ljava/lang/String; = "category"

.field public static final PREF_FIRSTRUN:Ljava/lang/String; = "firstrun"

.field public static final PREF_REMOTE:Ljava/lang/String; = "remote"

.field private static btn_catClicked_latest_categories:[Lmarto/androsdr2/presets/Category;

.field private static currCategory:Lmarto/androsdr2/presets/Category;

.field private static currPreset:Lmarto/androsdr2/presets/Preset;

.field private static forcePresetButtonsActiveStateRecheck:Z

.field private static latest_preset:Lmarto/androsdr2/presets/Preset;

.field private static final messages:[Lmarto/sdr/javasdr/SDRMessageFromServer;


# instance fields
.field private MODULATION_NAMES:[Lmarto/tools/ResourcedString;

.field private SUPPORTED_MODULATIONS_AND_NAMES:Ljava/util/List;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/List",
            "<",
            "Landroid/util/Pair",
            "<",
            "Ljava/lang/Runnable;",
            "Lmarto/tools/ResourcedString;",
            ">;>;"
        }
    .end annotation
.end field

.field private final actionShutDown:Lmarto/tools/macros/ShutDown;

.field private appLinkingInfo:Lmarto/tools/linking/OtherApps;

.field private btn_add:Landroid/widget/Button;

.field private btn_advancedrds:Landroid/widget/Button;

.field private btn_cat:Landroid/widget/Button;

.field private btn_catadd:I

.field private btn_catdelete:I

.field private btn_catrename:I

.field private btn_export:I

.field private btn_fft:Landroid/widget/Button;

.field private btn_gains:Landroid/widget/Button;

.field private btn_help:Landroid/widget/Button;

.field private btn_hide_favs:Landroid/widget/Button;

.field private btn_hide_menu:Landroid/widget/Button;

.field private btn_import:I

.field private btn_jump:Landroid/widget/Button;

.field private btn_modulation:Landroid/widget/Button;

.field private btn_off:Landroid/widget/Button;

.field private btn_onoff:Landroid/widget/Button;

.field private btn_open:Landroid/widget/Button;

.field private btn_prefs:Landroid/widget/Button;

.field private btn_rec:Landroid/widget/ToggleButton;

.field private btn_scan:Landroid/widget/ToggleButton;

.field private btn_show_favs:Landroid/widget/Button;

.field private btn_show_menu:Landroid/widget/Button;

.field private final btns_favs:Lmarto/tools/ExpandingArray;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Lmarto/tools/ExpandingArray",
            "<",
            "Lmarto/tools/gui/SDRPresetButton;",
            ">;"
        }
    .end annotation
.end field

.field private final btns_favs_sparse:Landroid/support/v4/util/SparseArrayCompat;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Landroid/support/v4/util/SparseArrayCompat",
            "<",
            "Lmarto/tools/gui/SDRPresetButton;",
            ">;"
        }
    .end annotation
.end field

.field private final favs_locker:Ljava/lang/Object;

.field private firstrun:Z

.field private isAudioBeingRecorded:Z

.field private isBasebandBeingRecorded:Z

.field private isPro:Z

.field private lastCatName:Ljava/lang/String;

.field private linlay_favs:Landroid/widget/LinearLayout;

.field private linlay_menu:Landroid/widget/LinearLayout;

.field private linlay_presetsplace:Landroid/widget/LinearLayout;

.field private mAudioGain:I

.field private mAutoGainSupported:Z

.field private mCentFreq:J

.field private mGain:I

.field private mGainManual:Z

.field private mGainSupported:Z

.field private mLPwidth:J

.field private mMod:Lmarto/sdr/javasdr/SDRRadio$MODULATION;

.field private mOffset:J

.field private mPpm:I

.field private mPpmSupported:Z

.field private mVFOFreq:J

.field private on:Z

.field private preset_db:Landroid/database/sqlite/SQLiteDatabase;

.field private preset_manager:Lmarto/androsdr2/presets/PresetDBManager;

.field private rdsPS:Ljava/lang/String;

.field private remote:Ljava/lang/String;

.field private scanner:Lmarto/androsdr2/presets/PresetScanner;

.field private final scanner_callback:Lmarto/androsdr2/presets/PresetScanner$ScannerCallback;

.field private sdrarea:Lmarto/tools/gui/SDRAreaDisplay_Android;

.field private shouldAutoStart:Z


# direct methods
.method static constructor <clinit>()V
    .locals 4

    .prologue
    const/4 v3, 0x1

    .line 94
    invoke-static {}, Ljava/util/Locale;->getDefault()Ljava/util/Locale;

    move-result-object v0

    sput-object v0, Lmarto/androsdr2/SDRTouchMain;->DEFAULT_LOCALE:Ljava/util/Locale;

    .line 109
    sput-boolean v3, Lmarto/androsdr2/SDRTouchMain;->forcePresetButtonsActiveStateRecheck:Z

    .line 155
    const/16 v0, 0x11

    new-array v0, v0, [Lmarto/sdr/javasdr/SDRMessageFromServer;

    const/4 v1, 0x0

    sget-object v2, Lmarto/sdr/javasdr/SDRMessageFromServer;->PLAYING:Lmarto/sdr/javasdr/SDRMessageFromServer;

    aput-object v2, v0, v1

    sget-object v1, Lmarto/sdr/javasdr/SDRMessageFromServer;->STOPPED:Lmarto/sdr/javasdr/SDRMessageFromServer;

    aput-object v1, v0, v3

    const/4 v1, 0x2

    sget-object v2, Lmarto/sdr/javasdr/SDRMessageFromServer;->EXCEPTION:Lmarto/sdr/javasdr/SDRMessageFromServer;

    aput-object v2, v0, v1

    const/4 v1, 0x3

    sget-object v2, Lmarto/sdr/javasdr/SDRMessageFromServer;->MODULATION_CHANGED:Lmarto/sdr/javasdr/SDRMessageFromServer;

    aput-object v2, v0, v1

    const/4 v1, 0x4

    sget-object v2, Lmarto/sdr/javasdr/SDRMessageFromServer;->CENTR_FREQ_CHANGED:Lmarto/sdr/javasdr/SDRMessageFromServer;

    aput-object v2, v0, v1

    const/4 v1, 0x5

    sget-object v2, Lmarto/sdr/javasdr/SDRMessageFromServer;->VFO_FREQ_CHANGED:Lmarto/sdr/javasdr/SDRMessageFromServer;

    aput-object v2, v0, v1

    const/4 v1, 0x6

    sget-object v2, Lmarto/sdr/javasdr/SDRMessageFromServer;->BASEBAND_LW_WIDTH_CHANGED:Lmarto/sdr/javasdr/SDRMessageFromServer;

    aput-object v2, v0, v1

    const/4 v1, 0x7

    sget-object v2, Lmarto/sdr/javasdr/SDRMessageFromServer;->OFFSET_CHANGED:Lmarto/sdr/javasdr/SDRMessageFromServer;

    aput-object v2, v0, v1

    const/16 v1, 0x8

    sget-object v2, Lmarto/sdr/javasdr/SDRMessageFromServer;->ON_GAIN_MANUAL_SET:Lmarto/sdr/javasdr/SDRMessageFromServer;

    aput-object v2, v0, v1

    const/16 v1, 0x9

    sget-object v2, Lmarto/sdr/javasdr/SDRMessageFromServer;->ON_GAIN_SET:Lmarto/sdr/javasdr/SDRMessageFromServer;

    aput-object v2, v0, v1

    const/16 v1, 0xa

    sget-object v2, Lmarto/sdr/javasdr/SDRMessageFromServer;->ON_PPM_SET:Lmarto/sdr/javasdr/SDRMessageFromServer;

    aput-object v2, v0, v1

    const/16 v1, 0xb

    sget-object v2, Lmarto/sdr/javasdr/SDRMessageFromServer;->ON_AUDIO_BOOST_SET:Lmarto/sdr/javasdr/SDRMessageFromServer;

    aput-object v2, v0, v1

    const/16 v1, 0xc

    sget-object v2, Lmarto/sdr/javasdr/SDRMessageFromServer;->ON_RECORDING_STOPPED:Lmarto/sdr/javasdr/SDRMessageFromServer;

    aput-object v2, v0, v1

    const/16 v1, 0xd

    sget-object v2, Lmarto/sdr/javasdr/SDRMessageFromServer;->ON_RECORDING_STATE_CHANGED:Lmarto/sdr/javasdr/SDRMessageFromServer;

    aput-object v2, v0, v1

    const/16 v1, 0xe

    sget-object v2, Lmarto/sdr/javasdr/SDRMessageFromServer;->FFT_SECONDS_REMAIN:Lmarto/sdr/javasdr/SDRMessageFromServer;

    aput-object v2, v0, v1

    const/16 v1, 0xf

    sget-object v2, Lmarto/sdr/javasdr/SDRMessageFromServer;->RDS_EVENT:Lmarto/sdr/javasdr/SDRMessageFromServer;

    aput-object v2, v0, v1

    const/16 v1, 0x10

    sget-object v2, Lmarto/sdr/javasdr/SDRMessageFromServer;->PRO_VERSION_CHANGED:Lmarto/sdr/javasdr/SDRMessageFromServer;

    aput-object v2, v0, v1

    sput-object v0, Lmarto/androsdr2/SDRTouchMain;->messages:[Lmarto/sdr/javasdr/SDRMessageFromServer;

    .line 191
    invoke-static {}, Lmarto/androsdr2/presets/Category;->getRoot()Lmarto/androsdr2/presets/Category;

    move-result-object v0

    sput-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    return-void
.end method

.method public constructor <init>()V
    .locals 3

    .prologue
    const/4 v1, 0x0

    const/4 v2, 0x0

    .line 63
    invoke-direct {p0}, Lmarto/sdr/javasdr/SDRRadioActivity;-><init>()V

    .line 102
    const-string v0, "127.0.0.1:1234"

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->remote:Ljava/lang/String;

    .line 103
    const/4 v0, 0x1

    iput-boolean v0, p0, Lmarto/androsdr2/SDRTouchMain;->firstrun:Z

    .line 104
    iput-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->lastCatName:Ljava/lang/String;

    .line 106
    iput-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->rdsPS:Ljava/lang/String;

    .line 107
    iput-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->isAudioBeingRecorded:Z

    iput-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->isBasebandBeingRecorded:Z

    .line 111
    new-instance v0, Lmarto/androsdr2/SDRTouchMain$1;

    invoke-direct {v0, p0}, Lmarto/androsdr2/SDRTouchMain$1;-><init>(Lmarto/androsdr2/SDRTouchMain;)V

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->scanner_callback:Lmarto/androsdr2/presets/PresetScanner$ScannerCallback;

    .line 126
    new-instance v0, Lmarto/tools/macros/ShutDown;

    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->comm:Lmarto/sdr/javasdr/SDRRadioActivity$SDRCommunicator;

    invoke-direct {v0, v1}, Lmarto/tools/macros/ShutDown;-><init>(Lmarto/tools/MessageClient;)V

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->actionShutDown:Lmarto/tools/macros/ShutDown;

    .line 175
    iput-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->on:Z

    .line 184
    new-instance v0, Lmarto/tools/ExpandingArray;

    const-class v1, Lmarto/tools/gui/SDRPresetButton;

    invoke-direct {v0, v1}, Lmarto/tools/ExpandingArray;-><init>(Ljava/lang/Class;)V

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btns_favs:Lmarto/tools/ExpandingArray;

    .line 185
    new-instance v0, Landroid/support/v4/util/SparseArrayCompat;

    invoke-direct {v0}, Landroid/support/v4/util/SparseArrayCompat;-><init>()V

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btns_favs_sparse:Landroid/support/v4/util/SparseArrayCompat;

    .line 186
    new-instance v0, Ljava/lang/Object;

    invoke-direct {v0}, Ljava/lang/Object;-><init>()V

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->favs_locker:Ljava/lang/Object;

    .line 200
    iput-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->isPro:Z

    .line 201
    iput-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->shouldAutoStart:Z

    return-void
.end method

.method static synthetic access$000(Lmarto/androsdr2/SDRTouchMain;)Landroid/widget/ToggleButton;
    .locals 1
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;

    .prologue
    .line 63
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_scan:Landroid/widget/ToggleButton;

    return-object v0
.end method

.method static synthetic access$100(Lmarto/androsdr2/SDRTouchMain;)V
    .locals 0
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;

    .prologue
    .line 63
    invoke-direct {p0}, Lmarto/androsdr2/SDRTouchMain;->checkWhetherSdrTouchWasSuspendedFromCurrentStore()V

    return-void
.end method

.method static synthetic access$1000(Lmarto/androsdr2/SDRTouchMain;)Landroid/widget/Button;
    .locals 1
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;

    .prologue
    .line 63
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_fft:Landroid/widget/Button;

    return-object v0
.end method

.method static synthetic access$1100(Lmarto/androsdr2/SDRTouchMain;Landroid/net/Uri;Z)V
    .locals 0
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;
    .param p1, "x1"    # Landroid/net/Uri;
    .param p2, "x2"    # Z

    .prologue
    .line 63
    invoke-direct {p0, p1, p2}, Lmarto/androsdr2/SDRTouchMain;->remoteStart(Landroid/net/Uri;Z)V

    return-void
.end method

.method static synthetic access$1200(Lmarto/androsdr2/SDRTouchMain;)Ljava/lang/Object;
    .locals 1
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;

    .prologue
    .line 63
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->favs_locker:Ljava/lang/Object;

    return-object v0
.end method

.method static synthetic access$1300(Lmarto/androsdr2/SDRTouchMain;)Lmarto/tools/ExpandingArray;
    .locals 1
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;

    .prologue
    .line 63
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btns_favs:Lmarto/tools/ExpandingArray;

    return-object v0
.end method

.method static synthetic access$1402(Lmarto/androsdr2/presets/Preset;)Lmarto/androsdr2/presets/Preset;
    .locals 0
    .param p0, "x0"    # Lmarto/androsdr2/presets/Preset;

    .prologue
    .line 63
    sput-object p0, Lmarto/androsdr2/SDRTouchMain;->currPreset:Lmarto/androsdr2/presets/Preset;

    return-object p0
.end method

.method static synthetic access$1502(Lmarto/androsdr2/presets/Preset;)Lmarto/androsdr2/presets/Preset;
    .locals 0
    .param p0, "x0"    # Lmarto/androsdr2/presets/Preset;

    .prologue
    .line 63
    sput-object p0, Lmarto/androsdr2/SDRTouchMain;->latest_preset:Lmarto/androsdr2/presets/Preset;

    return-object p0
.end method

.method static synthetic access$1600(Lmarto/androsdr2/SDRTouchMain;)Lmarto/androsdr2/presets/Preset;
    .locals 1
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;

    .prologue
    .line 63
    invoke-direct {p0}, Lmarto/androsdr2/SDRTouchMain;->buildLatestPreset()Lmarto/androsdr2/presets/Preset;

    move-result-object v0

    return-object v0
.end method

.method static synthetic access$1700(Lmarto/androsdr2/SDRTouchMain;ILjava/lang/String;[Ljava/lang/String;)V
    .locals 0
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;
    .param p1, "x1"    # I
    .param p2, "x2"    # Ljava/lang/String;
    .param p3, "x3"    # [Ljava/lang/String;

    .prologue
    .line 63
    invoke-virtual {p0, p1, p2, p3}, Lmarto/androsdr2/SDRTouchMain;->dialog_showItemsChooser(ILjava/lang/String;[Ljava/lang/String;)V

    return-void
.end method

.method static synthetic access$1800(Lmarto/androsdr2/SDRTouchMain;Ljava/lang/String;)Z
    .locals 1
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;
    .param p1, "x1"    # Ljava/lang/String;

    .prologue
    .line 63
    invoke-direct {p0, p1}, Lmarto/androsdr2/SDRTouchMain;->externalFileExists(Ljava/lang/String;)Z

    move-result v0

    return v0
.end method

.method static synthetic access$1900(Lmarto/androsdr2/SDRTouchMain;ILjava/lang/String;)V
    .locals 0
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;
    .param p1, "x1"    # I
    .param p2, "x2"    # Ljava/lang/String;

    .prologue
    .line 63
    invoke-virtual {p0, p1, p2}, Lmarto/androsdr2/SDRTouchMain;->dialog_showYesNo(ILjava/lang/String;)V

    return-void
.end method

.method static synthetic access$200(Lmarto/androsdr2/SDRTouchMain;)Z
    .locals 1
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;

    .prologue
    .line 63
    iget-boolean v0, p0, Lmarto/androsdr2/SDRTouchMain;->isAudioBeingRecorded:Z

    return v0
.end method

.method static synthetic access$2000(Lmarto/androsdr2/SDRTouchMain;)V
    .locals 0
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;

    .prologue
    .line 63
    invoke-direct {p0}, Lmarto/androsdr2/SDRTouchMain;->exportPresets()V

    return-void
.end method

.method static synthetic access$2100(Lmarto/androsdr2/SDRTouchMain;)Landroid/database/sqlite/SQLiteDatabase;
    .locals 1
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;

    .prologue
    .line 63
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->preset_db:Landroid/database/sqlite/SQLiteDatabase;

    return-object v0
.end method

.method static synthetic access$2200(Lmarto/androsdr2/SDRTouchMain;)V
    .locals 0
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;

    .prologue
    .line 63
    invoke-direct {p0}, Lmarto/androsdr2/SDRTouchMain;->importPresets()V

    return-void
.end method

.method static synthetic access$2300(Lmarto/androsdr2/SDRTouchMain;Ljava/util/Collection;)Ljava/lang/String;
    .locals 1
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;
    .param p1, "x1"    # Ljava/util/Collection;

    .prologue
    .line 63
    invoke-direct {p0, p1}, Lmarto/androsdr2/SDRTouchMain;->convertPrestsToString(Ljava/util/Collection;)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method static synthetic access$2400(Lmarto/androsdr2/SDRTouchMain;ILjava/lang/String;)V
    .locals 0
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;
    .param p1, "x1"    # I
    .param p2, "x2"    # Ljava/lang/String;

    .prologue
    .line 63
    invoke-virtual {p0, p1, p2}, Lmarto/androsdr2/SDRTouchMain;->dialog_showYesNo(ILjava/lang/String;)V

    return-void
.end method

.method static synthetic access$2500(Lmarto/androsdr2/SDRTouchMain;ILjava/lang/String;)V
    .locals 0
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;
    .param p1, "x1"    # I
    .param p2, "x2"    # Ljava/lang/String;

    .prologue
    .line 63
    invoke-virtual {p0, p1, p2}, Lmarto/androsdr2/SDRTouchMain;->dialog_showYesNo(ILjava/lang/String;)V

    return-void
.end method

.method static synthetic access$2600(Lmarto/androsdr2/SDRTouchMain;Ljava/lang/String;Ljava/lang/String;)V
    .locals 0
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;
    .param p1, "x1"    # Ljava/lang/String;
    .param p2, "x2"    # Ljava/lang/String;

    .prologue
    .line 63
    invoke-virtual {p0, p1, p2}, Lmarto/androsdr2/SDRTouchMain;->dialog_showInfo(Ljava/lang/String;Ljava/lang/String;)V

    return-void
.end method

.method static synthetic access$300(Lmarto/androsdr2/SDRTouchMain;)Z
    .locals 1
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;

    .prologue
    .line 63
    iget-boolean v0, p0, Lmarto/androsdr2/SDRTouchMain;->isBasebandBeingRecorded:Z

    return v0
.end method

.method static synthetic access$400(Lmarto/androsdr2/SDRTouchMain;)Landroid/widget/ToggleButton;
    .locals 1
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;

    .prologue
    .line 63
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_rec:Landroid/widget/ToggleButton;

    return-object v0
.end method

.method static synthetic access$500(Lmarto/androsdr2/SDRTouchMain;Lmarto/sdr/javasdr/SDRMessageFromClient;JJ)V
    .locals 0
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;
    .param p1, "x1"    # Lmarto/sdr/javasdr/SDRMessageFromClient;
    .param p2, "x2"    # J
    .param p4, "x3"    # J

    .prologue
    .line 63
    invoke-virtual/range {p0 .. p5}, Lmarto/androsdr2/SDRTouchMain;->sdrSendMessageToServer(Lmarto/sdr/javasdr/SDRMessageFromClient;JJ)V

    return-void
.end method

.method static synthetic access$600(Lmarto/androsdr2/SDRTouchMain;Lmarto/sdr/javasdr/SDRMessageFromClient;JJ)V
    .locals 0
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;
    .param p1, "x1"    # Lmarto/sdr/javasdr/SDRMessageFromClient;
    .param p2, "x2"    # J
    .param p4, "x3"    # J

    .prologue
    .line 63
    invoke-virtual/range {p0 .. p5}, Lmarto/androsdr2/SDRTouchMain;->sdrSendMessageToServer(Lmarto/sdr/javasdr/SDRMessageFromClient;JJ)V

    return-void
.end method

.method static synthetic access$700(Lmarto/androsdr2/SDRTouchMain;ILjava/lang/String;[Ljava/lang/String;)V
    .locals 0
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;
    .param p1, "x1"    # I
    .param p2, "x2"    # Ljava/lang/String;
    .param p3, "x3"    # [Ljava/lang/String;

    .prologue
    .line 63
    invoke-virtual {p0, p1, p2, p3}, Lmarto/androsdr2/SDRTouchMain;->dialog_showItemsChooser(ILjava/lang/String;[Ljava/lang/String;)V

    return-void
.end method

.method static synthetic access$800(Lmarto/androsdr2/SDRTouchMain;)Landroid/widget/Button;
    .locals 1
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;

    .prologue
    .line 63
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_modulation:Landroid/widget/Button;

    return-object v0
.end method

.method static synthetic access$900(Lmarto/androsdr2/SDRTouchMain;)Landroid/widget/Button;
    .locals 1
    .param p0, "x0"    # Lmarto/androsdr2/SDRTouchMain;

    .prologue
    .line 63
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_advancedrds:Landroid/widget/Button;

    return-object v0
.end method

.method private btn_addClicked()V
    .locals 11

    .prologue
    const/4 v10, 0x1

    .line 801
    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->rdsPS:Ljava/lang/String;

    if-eqz v1, :cond_0

    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->rdsPS:Ljava/lang/String;

    .line 802
    .local v0, "name":Ljava/lang/String;
    :goto_0
    const v1, 0x7f0700c8

    invoke-virtual {p0, v1}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {p0, v10, v1, v0}, Lmarto/androsdr2/SDRTouchMain;->dialog_showTextInput(ILjava/lang/String;Ljava/lang/String;)V

    .line 803
    invoke-direct {p0}, Lmarto/androsdr2/SDRTouchMain;->buildLatestPreset()Lmarto/androsdr2/presets/Preset;

    move-result-object v1

    sput-object v1, Lmarto/androsdr2/SDRTouchMain;->latest_preset:Lmarto/androsdr2/presets/Preset;

    .line 804
    return-void

    .line 801
    .end local v0    # "name":Ljava/lang/String;
    :cond_0
    sget-object v1, Lmarto/androsdr2/SDRTouchMain;->DEFAULT_LOCALE:Ljava/util/Locale;

    const-string v2, "%.1f %s"

    const/4 v3, 0x2

    new-array v3, v3, [Ljava/lang/Object;

    const/4 v4, 0x0

    iget-wide v6, p0, Lmarto/androsdr2/SDRTouchMain;->mCentFreq:J

    iget-wide v8, p0, Lmarto/androsdr2/SDRTouchMain;->mVFOFreq:J

    add-long/2addr v6, v8

    long-to-double v6, v6

    const-wide v8, 0x412e848000000000L    # 1000000.0

    div-double/2addr v6, v8

    invoke-static {v6, v7}, Ljava/lang/Double;->valueOf(D)Ljava/lang/Double;

    move-result-object v5

    aput-object v5, v3, v4

    iget-object v4, p0, Lmarto/androsdr2/SDRTouchMain;->mMod:Lmarto/sdr/javasdr/SDRRadio$MODULATION;

    invoke-virtual {v4}, Lmarto/sdr/javasdr/SDRRadio$MODULATION;->toString()Ljava/lang/String;

    move-result-object v4

    aput-object v4, v3, v10

    invoke-static {v1, v2, v3}, Ljava/lang/String;->format(Ljava/util/Locale;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v0

    goto :goto_0
.end method

.method private btn_catClicked()V
    .locals 8

    .prologue
    const/4 v7, 0x1

    const/4 v4, -0x1

    const/4 v6, 0x0

    .line 809
    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    if-nez v2, :cond_0

    .line 810
    new-instance v2, Ljava/lang/RuntimeException;

    const-string v3, "Cannot show preset."

    invoke-direct {v2, v3}, Ljava/lang/RuntimeException;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0, v2}, Lmarto/androsdr2/SDRTouchMain;->onException(Ljava/lang/Exception;)V

    .line 841
    :goto_0
    return-void

    .line 814
    :cond_0
    iget-object v2, p0, Lmarto/androsdr2/SDRTouchMain;->preset_db:Landroid/database/sqlite/SQLiteDatabase;

    invoke-static {v2}, Lmarto/androsdr2/presets/PresetDBManager;->getAllCategories(Landroid/database/sqlite/SQLiteDatabase;)Ljava/util/Collection;

    move-result-object v2

    new-array v3, v6, [Lmarto/androsdr2/presets/Category;

    invoke-interface {v2, v3}, Ljava/util/Collection;->toArray([Ljava/lang/Object;)[Ljava/lang/Object;

    move-result-object v2

    check-cast v2, [Lmarto/androsdr2/presets/Category;

    sput-object v2, Lmarto/androsdr2/SDRTouchMain;->btn_catClicked_latest_categories:[Lmarto/androsdr2/presets/Category;

    .line 815
    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->btn_catClicked_latest_categories:[Lmarto/androsdr2/presets/Category;

    array-length v3, v2

    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    invoke-virtual {v2}, Lmarto/androsdr2/presets/Category;->isRoot()Z

    move-result v2

    if-eqz v2, :cond_1

    const/4 v2, 0x3

    :goto_1
    add-int/2addr v2, v3

    new-array v1, v2, [Ljava/lang/String;

    .line 816
    .local v1, "options":[Ljava/lang/String;
    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    invoke-virtual {v2}, Lmarto/androsdr2/presets/Category;->isRoot()Z

    move-result v2

    if-eqz v2, :cond_2

    .line 817
    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->btn_catClicked_latest_categories:[Lmarto/androsdr2/presets/Category;

    array-length v2, v2

    iput v2, p0, Lmarto/androsdr2/SDRTouchMain;->btn_catadd:I

    .line 818
    iput v4, p0, Lmarto/androsdr2/SDRTouchMain;->btn_catdelete:I

    .line 819
    iput v4, p0, Lmarto/androsdr2/SDRTouchMain;->btn_catrename:I

    .line 820
    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->btn_catClicked_latest_categories:[Lmarto/androsdr2/presets/Category;

    array-length v2, v2

    add-int/lit8 v2, v2, 0x1

    iput v2, p0, Lmarto/androsdr2/SDRTouchMain;->btn_export:I

    .line 821
    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->btn_catClicked_latest_categories:[Lmarto/androsdr2/presets/Category;

    array-length v2, v2

    add-int/lit8 v2, v2, 0x2

    iput v2, p0, Lmarto/androsdr2/SDRTouchMain;->btn_import:I

    .line 830
    :goto_2
    const/4 v0, 0x0

    .local v0, "i":I
    :goto_3
    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->btn_catClicked_latest_categories:[Lmarto/androsdr2/presets/Category;

    array-length v2, v2

    if-ge v0, v2, :cond_3

    .line 831
    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->btn_catClicked_latest_categories:[Lmarto/androsdr2/presets/Category;

    aget-object v2, v2, v0

    iget-object v2, v2, Lmarto/androsdr2/presets/Category;->name:Ljava/lang/String;

    aput-object v2, v1, v0

    .line 830
    add-int/lit8 v0, v0, 0x1

    goto :goto_3

    .line 815
    .end local v0    # "i":I
    .end local v1    # "options":[Ljava/lang/String;
    :cond_1
    const/4 v2, 0x5

    goto :goto_1

    .line 823
    .restart local v1    # "options":[Ljava/lang/String;
    :cond_2
    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->btn_catClicked_latest_categories:[Lmarto/androsdr2/presets/Category;

    array-length v2, v2

    iput v2, p0, Lmarto/androsdr2/SDRTouchMain;->btn_catrename:I

    .line 824
    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->btn_catClicked_latest_categories:[Lmarto/androsdr2/presets/Category;

    array-length v2, v2

    add-int/lit8 v2, v2, 0x1

    iput v2, p0, Lmarto/androsdr2/SDRTouchMain;->btn_catdelete:I

    .line 825
    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->btn_catClicked_latest_categories:[Lmarto/androsdr2/presets/Category;

    array-length v2, v2

    add-int/lit8 v2, v2, 0x2

    iput v2, p0, Lmarto/androsdr2/SDRTouchMain;->btn_catadd:I

    .line 826
    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->btn_catClicked_latest_categories:[Lmarto/androsdr2/presets/Category;

    array-length v2, v2

    add-int/lit8 v2, v2, 0x3

    iput v2, p0, Lmarto/androsdr2/SDRTouchMain;->btn_export:I

    .line 827
    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->btn_catClicked_latest_categories:[Lmarto/androsdr2/presets/Category;

    array-length v2, v2

    add-int/lit8 v2, v2, 0x4

    iput v2, p0, Lmarto/androsdr2/SDRTouchMain;->btn_import:I

    goto :goto_2

    .line 833
    .restart local v0    # "i":I
    :cond_3
    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    invoke-virtual {v2}, Lmarto/androsdr2/presets/Category;->isRoot()Z

    move-result v2

    if-nez v2, :cond_4

    .line 834
    iget v2, p0, Lmarto/androsdr2/SDRTouchMain;->btn_catrename:I

    const v3, 0x7f070074

    new-array v4, v7, [Ljava/lang/Object;

    sget-object v5, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    iget-object v5, v5, Lmarto/androsdr2/presets/Category;->name:Ljava/lang/String;

    aput-object v5, v4, v6

    invoke-virtual {p0, v3, v4}, Lmarto/androsdr2/SDRTouchMain;->getString(I[Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v3

    aput-object v3, v1, v2

    .line 835
    iget v2, p0, Lmarto/androsdr2/SDRTouchMain;->btn_catdelete:I

    const v3, 0x7f070080

    new-array v4, v7, [Ljava/lang/Object;

    sget-object v5, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    iget-object v5, v5, Lmarto/androsdr2/presets/Category;->name:Ljava/lang/String;

    aput-object v5, v4, v6

    invoke-virtual {p0, v3, v4}, Lmarto/androsdr2/SDRTouchMain;->getString(I[Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v3

    aput-object v3, v1, v2

    .line 837
    :cond_4
    iget v2, p0, Lmarto/androsdr2/SDRTouchMain;->btn_catadd:I

    const v3, 0x7f07007c

    invoke-virtual {p0, v3}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v3

    aput-object v3, v1, v2

    .line 838
    iget v2, p0, Lmarto/androsdr2/SDRTouchMain;->btn_export:I

    const v3, 0x7f070082

    invoke-virtual {p0, v3}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v3

    aput-object v3, v1, v2

    .line 839
    iget v2, p0, Lmarto/androsdr2/SDRTouchMain;->btn_import:I

    const v3, 0x7f070083

    invoke-virtual {p0, v3}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v3

    aput-object v3, v1, v2

    .line 840
    const/4 v2, 0x2

    const v3, 0x7f07007e

    invoke-virtual {p0, v3}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {p0, v2, v3, v1}, Lmarto/androsdr2/SDRTouchMain;->dialog_showItemsChooser(ILjava/lang/String;[Ljava/lang/String;)V

    goto/16 :goto_0
.end method

.method private btn_catClicked_result(I)V
    .locals 7
    .param p1, "id"    # I

    .prologue
    const/4 v6, 0x0

    const/4 v5, 0x1

    .line 844
    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    if-nez v2, :cond_0

    .line 845
    new-instance v2, Ljava/lang/RuntimeException;

    const-string v3, "Cannot invoke category menu."

    invoke-direct {v2, v3}, Ljava/lang/RuntimeException;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0, v2}, Lmarto/androsdr2/SDRTouchMain;->onException(Ljava/lang/Exception;)V

    .line 900
    :goto_0
    return-void

    .line 849
    :cond_0
    iget v2, p0, Lmarto/androsdr2/SDRTouchMain;->btn_catdelete:I

    if-ne p1, v2, :cond_1

    .line 850
    const v2, 0x7f070081

    new-array v3, v5, [Ljava/lang/Object;

    sget-object v4, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    iget-object v4, v4, Lmarto/androsdr2/presets/Category;->name:Ljava/lang/String;

    aput-object v4, v3, v6

    invoke-virtual {p0, v2, v3}, Lmarto/androsdr2/SDRTouchMain;->getString(I[Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v2

    invoke-virtual {p0, v5, v2}, Lmarto/androsdr2/SDRTouchMain;->dialog_showYesNo(ILjava/lang/String;)V

    goto :goto_0

    .line 851
    :cond_1
    iget v2, p0, Lmarto/androsdr2/SDRTouchMain;->btn_catadd:I

    if-ne p1, v2, :cond_2

    .line 852
    const/4 v2, 0x2

    const v3, 0x7f07007d

    invoke-virtual {p0, v3}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v3

    const v4, 0x7f07007f

    invoke-virtual {p0, v4}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v4

    invoke-virtual {p0, v2, v3, v4}, Lmarto/androsdr2/SDRTouchMain;->dialog_showTextInput(ILjava/lang/String;Ljava/lang/String;)V

    goto :goto_0

    .line 853
    :cond_2
    iget v2, p0, Lmarto/androsdr2/SDRTouchMain;->btn_catrename:I

    if-ne p1, v2, :cond_3

    .line 854
    const/4 v2, 0x4

    const v3, 0x7f070074

    new-array v4, v5, [Ljava/lang/Object;

    sget-object v5, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    iget-object v5, v5, Lmarto/androsdr2/presets/Category;->name:Ljava/lang/String;

    aput-object v5, v4, v6

    invoke-virtual {p0, v3, v4}, Lmarto/androsdr2/SDRTouchMain;->getString(I[Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v3

    sget-object v4, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    iget-object v4, v4, Lmarto/androsdr2/presets/Category;->name:Ljava/lang/String;

    invoke-virtual {p0, v2, v3, v4}, Lmarto/androsdr2/SDRTouchMain;->dialog_showTextInput(ILjava/lang/String;Ljava/lang/String;)V

    goto :goto_0

    .line 855
    :cond_3
    iget v2, p0, Lmarto/androsdr2/SDRTouchMain;->btn_export:I

    if-ne p1, v2, :cond_4

    .line 856
    new-instance v0, Lmarto/androsdr2/SDRTouchMain$12;

    invoke-direct {v0, p0}, Lmarto/androsdr2/SDRTouchMain$12;-><init>(Lmarto/androsdr2/SDRTouchMain;)V

    .line 865
    .local v0, "btn_export_action":Ljava/lang/Runnable;
    iget-object v2, p0, Lmarto/androsdr2/SDRTouchMain;->permissionObtainer:Lmarto/sdr/javasdr/RuntimePermissionObtainer;

    const-string v3, "android.permission.WRITE_EXTERNAL_STORAGE"

    invoke-virtual {v2, v3, v0}, Lmarto/sdr/javasdr/RuntimePermissionObtainer;->runIfPermissionAvailable(Ljava/lang/String;Ljava/lang/Runnable;)V

    goto :goto_0

    .line 866
    .end local v0    # "btn_export_action":Ljava/lang/Runnable;
    :cond_4
    iget v2, p0, Lmarto/androsdr2/SDRTouchMain;->btn_import:I

    if-ne p1, v2, :cond_6

    .line 867
    new-instance v1, Lmarto/androsdr2/SDRTouchMain$13;

    invoke-direct {v1, p0}, Lmarto/androsdr2/SDRTouchMain$13;-><init>(Lmarto/androsdr2/SDRTouchMain;)V

    .line 891
    .local v1, "btn_import_action":Ljava/lang/Runnable;
    sget v2, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v3, 0x10

    if-lt v2, v3, :cond_5

    .line 892
    iget-object v2, p0, Lmarto/androsdr2/SDRTouchMain;->permissionObtainer:Lmarto/sdr/javasdr/RuntimePermissionObtainer;

    const-string v3, "android.permission.READ_EXTERNAL_STORAGE"

    invoke-virtual {v2, v3, v1}, Lmarto/sdr/javasdr/RuntimePermissionObtainer;->runIfPermissionAvailable(Ljava/lang/String;Ljava/lang/Runnable;)V

    goto :goto_0

    .line 894
    :cond_5
    invoke-interface {v1}, Ljava/lang/Runnable;->run()V

    goto :goto_0

    .line 897
    .end local v1    # "btn_import_action":Ljava/lang/Runnable;
    :cond_6
    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->btn_catClicked_latest_categories:[Lmarto/androsdr2/presets/Category;

    aget-object v2, v2, p1

    sput-object v2, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    .line 898
    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    invoke-direct {p0, v2}, Lmarto/androsdr2/SDRTouchMain;->createAllButtonsFor(Lmarto/androsdr2/presets/Category;)V


	#ahat
	#from http://androidcracking.blogspot.gr/2010/09/examplesmali.html
	
	# create instance of StringBuilder in v1
	#new-instance v1, Ljava/lang/StringBuilder;

	# initialize StringBuilder with v3
	# notice it returns V, or void
	#const-string v3, "Current Category: "
	#invoke-direct {v1, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

	# get the current category name, the current category is already in v2
	iget-object v3, v2, Lmarto/androsdr2/presets/Category;->name:Ljava/lang/String;

	# append v3 to our StringBuilder
	#invoke-virtual {v1, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
	#move-result-object v1

	# call toString() on our StringBuilder
	#invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
	#move-result-object v1

	#const/4 v0, 0x1

	#invoke-static {p0, v1, v0}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

	#move-result-object v0

	#invoke-virtual {v0}, Landroid/widget/Toast;->show()V



	new-instance v0, Landroid/content/Intent;
    const-string v1, "ahat.custom.intent.SDR_CATEGORY"
	invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

	const-string v2, "name"
	invoke-virtual {v0, v2, v3}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

	const/4 v4, 0x0
	invoke-virtual {p0, v0, v4}, Lmarto/androsdr2/SDRTouchMain;->sendOrderedBroadcast(Landroid/content/Intent;Ljava/lang/String;)V
		
	#const-string v1, "Also sent ahat.custom.intent.SDR_CATEGORY"
	#const/4 v0, 0x1

	#invoke-static {p0, v1, v0}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

	#move-result-object v0

	#invoke-virtual {v0}, Landroid/widget/Toast;->show()V

	#ahat

    goto/16 :goto_0

.end method

.method private buildLatestPreset()Lmarto/androsdr2/presets/Preset;
    .locals 12

    .prologue
    .line 797
    new-instance v1, Lmarto/androsdr2/presets/Preset;

    iget-wide v2, p0, Lmarto/androsdr2/SDRTouchMain;->mCentFreq:J

    iget-wide v4, p0, Lmarto/androsdr2/SDRTouchMain;->mVFOFreq:J

    add-long/2addr v2, v4

    iget-wide v4, p0, Lmarto/androsdr2/SDRTouchMain;->mCentFreq:J

    iget-wide v6, p0, Lmarto/androsdr2/SDRTouchMain;->mOffset:J

    sget-object v8, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->mMod:Lmarto/sdr/javasdr/SDRRadio$MODULATION;

    invoke-virtual {v0}, Lmarto/sdr/javasdr/SDRRadio$MODULATION;->ordinal()I

    move-result v9

    iget-wide v10, p0, Lmarto/androsdr2/SDRTouchMain;->mLPwidth:J

    invoke-direct/range {v1 .. v11}, Lmarto/androsdr2/presets/Preset;-><init>(JJJLmarto/androsdr2/presets/Category;IJ)V

    return-object v1
.end method

.method private checkWhetherSdrTouchWasSuspendedFromCurrentStore()V
    .locals 4
    .annotation build Landroid/support/annotation/UiThread;
    .end annotation

    .prologue
    .line 288
    sget-object v1, Lmarto/tools/linking/AppStore;->THIS:Lmarto/tools/linking/AppStore;

    .line 289
    .local v1, "expectedSdrTouchAppStore":Lmarto/tools/linking/AppStore;
    iget-object v2, p0, Lmarto/androsdr2/SDRTouchMain;->appLinkingInfo:Lmarto/tools/linking/OtherApps;

    sget-object v3, Lmarto/tools/linking/OtherApps$App;->SDR_TOUCH:Lmarto/tools/linking/OtherApps$App;

    invoke-virtual {v2, v3}, Lmarto/tools/linking/OtherApps;->getAppStoreFor(Lmarto/tools/linking/OtherApps$App;)Lmarto/tools/linking/AppStore;

    move-result-object v0

    .line 291
    .local v0, "actualSdrTouchAppStore":Lmarto/tools/linking/AppStore;
    if-eqz v0, :cond_0

    invoke-virtual {v0, v1}, Lmarto/tools/linking/AppStore;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-nez v2, :cond_0

    .line 293
    const/4 v2, 0x5

    const v3, 0x7f07010c

    invoke-virtual {p0, v3}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {p0, v2, v3}, Lmarto/androsdr2/SDRTouchMain;->dialog_showYesNo(ILjava/lang/String;)V

    .line 295
    :cond_0
    return-void
.end method

.method private convertPrestsToString(Ljava/util/Collection;)Ljava/lang/String;
    .locals 8
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/util/Collection",
            "<",
            "Lmarto/androsdr2/presets/Preset;",
            ">;)",
            "Ljava/lang/String;"
        }
    .end annotation

    .prologue
    .local p1, "endangeredPresets":Ljava/util/Collection;, "Ljava/util/Collection<Lmarto/androsdr2/presets/Preset;>;"
    const v7, 0x7f070075

    .line 903
    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    .line 904
    .local v3, "preset_names":Ljava/lang/StringBuilder;
    invoke-interface {p1}, Ljava/util/Collection;->size()I

    move-result v1

    .line 905
    .local v1, "length":I
    const/4 v0, 0x0

    .line 906
    .local v0, "i":I
    invoke-interface {p1}, Ljava/util/Collection;->iterator()Ljava/util/Iterator;

    move-result-object v4

    :goto_0
    invoke-interface {v4}, Ljava/util/Iterator;->hasNext()Z

    move-result v5

    if-eqz v5, :cond_5

    invoke-interface {v4}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Lmarto/androsdr2/presets/Preset;

    .line 908
    .local v2, "p":Lmarto/androsdr2/presets/Preset;
    iget-object v5, v2, Lmarto/androsdr2/presets/Preset;->cat:Lmarto/androsdr2/presets/Category;

    invoke-virtual {v5}, Lmarto/androsdr2/presets/Category;->isRoot()Z

    move-result v5

    if-eqz v5, :cond_2

    .line 909
    if-nez v0, :cond_0

    .line 910
    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    const-string v6, "\'"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    iget-object v6, v2, Lmarto/androsdr2/presets/Preset;->name:Ljava/lang/String;

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v6, "\'"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v3, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 923
    :goto_1
    add-int/lit8 v0, v0, 0x1

    .line 924
    goto :goto_0

    .line 911
    :cond_0
    add-int/lit8 v5, v1, -0x1

    if-ne v0, v5, :cond_1

    .line 912
    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    const-string v6, " "

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {p0, v7}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v6, " \'"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    iget-object v6, v2, Lmarto/androsdr2/presets/Preset;->name:Ljava/lang/String;

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v6, "\'"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v3, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    goto :goto_1

    .line 914
    :cond_1
    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    const-string v6, ", \'"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    iget-object v6, v2, Lmarto/androsdr2/presets/Preset;->name:Ljava/lang/String;

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v6, "\'"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v3, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    goto :goto_1

    .line 916
    :cond_2
    if-nez v0, :cond_3

    .line 917
    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    const-string v6, "\'"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    iget-object v6, v2, Lmarto/androsdr2/presets/Preset;->name:Ljava/lang/String;

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v6, "\' ("

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    iget-object v6, v2, Lmarto/androsdr2/presets/Preset;->cat:Lmarto/androsdr2/presets/Category;

    iget-object v6, v6, Lmarto/androsdr2/presets/Category;->name:Ljava/lang/String;

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v6, ")"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v3, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    goto/16 :goto_1

    .line 918
    :cond_3
    add-int/lit8 v5, v1, -0x1

    if-ne v0, v5, :cond_4

    .line 919
    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    const-string v6, " "

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {p0, v7}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v6, " \'"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    iget-object v6, v2, Lmarto/androsdr2/presets/Preset;->name:Ljava/lang/String;

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v6, "\' ("

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    iget-object v6, v2, Lmarto/androsdr2/presets/Preset;->cat:Lmarto/androsdr2/presets/Category;

    iget-object v6, v6, Lmarto/androsdr2/presets/Category;->name:Ljava/lang/String;

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v6, ")"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v3, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    goto/16 :goto_1

    .line 921
    :cond_4
    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    const-string v6, ", \'"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    iget-object v6, v2, Lmarto/androsdr2/presets/Preset;->name:Ljava/lang/String;

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v6, "\' ("

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    iget-object v6, v2, Lmarto/androsdr2/presets/Preset;->cat:Lmarto/androsdr2/presets/Category;

    iget-object v6, v6, Lmarto/androsdr2/presets/Category;->name:Ljava/lang/String;

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v6, ")"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v3, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    goto/16 :goto_1

    .line 925
    .end local v2    # "p":Lmarto/androsdr2/presets/Preset;
    :cond_5
    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    return-object v4
.end method

.method private createAllButtonsFor(Lmarto/androsdr2/presets/Category;)V
    .locals 14
    .param p1, "cat"    # Lmarto/androsdr2/presets/Category;
    .annotation build Landroid/annotation/SuppressLint;
        value = {
            "InflateParams"
        }
    .end annotation

    .prologue
    .line 722
    if-nez p1, :cond_0

    invoke-static {}, Lmarto/androsdr2/presets/Category;->getRoot()Lmarto/androsdr2/presets/Category;

    move-result-object p1

    .line 723
    :cond_0
    iget-object v7, p0, Lmarto/androsdr2/SDRTouchMain;->favs_locker:Ljava/lang/Object;

    monitor-enter v7

    .line 724
    :try_start_0
    iget-object v6, p0, Lmarto/androsdr2/SDRTouchMain;->btn_cat:Landroid/widget/Button;

    iget-object v8, p1, Lmarto/androsdr2/presets/Category;->name:Ljava/lang/String;

    invoke-virtual {v6, v8}, Landroid/widget/Button;->setText(Ljava/lang/CharSequence;)V

    .line 726
    iget-object v6, p0, Lmarto/androsdr2/SDRTouchMain;->btns_favs:Lmarto/tools/ExpandingArray;

    invoke-virtual {v6}, Lmarto/tools/ExpandingArray;->getAndLock()[Ljava/lang/Object;

    move-result-object v1

    check-cast v1, [Lmarto/tools/gui/SDRPresetButton;
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 728
    .local v1, "btns":[Lmarto/tools/gui/SDRPresetButton;
    :try_start_1
    iget-object v6, p0, Lmarto/androsdr2/SDRTouchMain;->btns_favs:Lmarto/tools/ExpandingArray;

    invoke-virtual {v6}, Lmarto/tools/ExpandingArray;->size()I

    move-result v5

    .line 729
    .local v5, "size":I
    const/4 v2, 0x0

    .local v2, "i":I
    :goto_0
    if-ge v2, v5, :cond_1

    .line 730
    iget-object v6, p0, Lmarto/androsdr2/SDRTouchMain;->linlay_presetsplace:Landroid/widget/LinearLayout;

    aget-object v8, v1, v2

    invoke-virtual {v6, v8}, Landroid/widget/LinearLayout;->removeView(Landroid/view/View;)V
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_1

    .line 729
    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    .line 732
    :cond_1
    :try_start_2
    iget-object v6, p0, Lmarto/androsdr2/SDRTouchMain;->btns_favs:Lmarto/tools/ExpandingArray;

    invoke-virtual {v6}, Lmarto/tools/ExpandingArray;->unlock()V

    .line 735
    iget-object v6, p0, Lmarto/androsdr2/SDRTouchMain;->linlay_presetsplace:Landroid/widget/LinearLayout;

    iget-object v8, p0, Lmarto/androsdr2/SDRTouchMain;->btn_add:Landroid/widget/Button;

    invoke-virtual {v6, v8}, Landroid/widget/LinearLayout;->removeView(Landroid/view/View;)V

    .line 736
    iget-object v6, p0, Lmarto/androsdr2/SDRTouchMain;->btns_favs:Lmarto/tools/ExpandingArray;

    invoke-virtual {v6}, Lmarto/tools/ExpandingArray;->clear()V

    .line 737
    iget-object v6, p0, Lmarto/androsdr2/SDRTouchMain;->btns_favs_sparse:Landroid/support/v4/util/SparseArrayCompat;

    invoke-virtual {v6}, Landroid/support/v4/util/SparseArrayCompat;->clear()V

    .line 739
    iget-object v6, p0, Lmarto/androsdr2/SDRTouchMain;->preset_db:Landroid/database/sqlite/SQLiteDatabase;

    invoke-static {p1, v6}, Lmarto/androsdr2/presets/PresetDBManager;->getAllPresets(Lmarto/androsdr2/presets/Category;Landroid/database/sqlite/SQLiteDatabase;)Ljava/util/Collection;

    move-result-object v4

    .line 740
    .local v4, "presets":Ljava/util/Collection;, "Ljava/util/Collection<Lmarto/androsdr2/presets/Preset;>;"
    invoke-interface {v4}, Ljava/util/Collection;->iterator()Ljava/util/Iterator;

    move-result-object v6

    :goto_1
    invoke-interface {v6}, Ljava/util/Iterator;->hasNext()Z

    move-result v8

    if-eqz v8, :cond_2

    invoke-interface {v6}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v3

    check-cast v3, Lmarto/androsdr2/presets/Preset;

    .line 741
    .local v3, "p":Lmarto/androsdr2/presets/Preset;
    invoke-virtual {p0}, Lmarto/androsdr2/SDRTouchMain;->getLayoutInflater()Landroid/view/LayoutInflater;

    move-result-object v8

    const v9, 0x7f03002f

    const/4 v10, 0x0

    invoke-virtual {v8, v9, v10}, Landroid/view/LayoutInflater;->inflate(ILandroid/view/ViewGroup;)Landroid/view/View;

    move-result-object v0

    check-cast v0, Lmarto/tools/gui/SDRPresetButton;

    .line 742
    .local v0, "btn":Lmarto/tools/gui/SDRPresetButton;
    invoke-virtual {v0, v3}, Lmarto/tools/gui/SDRPresetButton;->setPreset(Lmarto/androsdr2/presets/Preset;)V

    .line 743
    iget-object v8, p0, Lmarto/androsdr2/SDRTouchMain;->btns_favs:Lmarto/tools/ExpandingArray;

    invoke-virtual {v8, v0}, Lmarto/tools/ExpandingArray;->add(Ljava/lang/Object;)Z

    .line 744
    iget-object v8, p0, Lmarto/androsdr2/SDRTouchMain;->btns_favs_sparse:Landroid/support/v4/util/SparseArrayCompat;

    iget-wide v10, v3, Lmarto/androsdr2/presets/Preset;->freq:J

    const-wide/16 v12, 0x3e8

    div-long/2addr v10, v12

    long-to-int v9, v10

    invoke-virtual {v8, v9, v0}, Landroid/support/v4/util/SparseArrayCompat;->append(ILjava/lang/Object;)V

    .line 745
    new-instance v8, Lmarto/androsdr2/SDRTouchMain$11;

    invoke-direct {v8, p0, v3}, Lmarto/androsdr2/SDRTouchMain$11;-><init>(Lmarto/androsdr2/SDRTouchMain;Lmarto/androsdr2/presets/Preset;)V

    invoke-virtual {v0, v8}, Lmarto/tools/gui/SDRPresetButton;->setOnLongClickListener(Landroid/view/View$OnLongClickListener;)V

    .line 756
    iget-object v8, p0, Lmarto/androsdr2/SDRTouchMain;->linlay_presetsplace:Landroid/widget/LinearLayout;

    invoke-virtual {v8, v0}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;)V

    goto :goto_1

    .line 760
    .end local v0    # "btn":Lmarto/tools/gui/SDRPresetButton;
    .end local v1    # "btns":[Lmarto/tools/gui/SDRPresetButton;
    .end local v2    # "i":I
    .end local v3    # "p":Lmarto/androsdr2/presets/Preset;
    .end local v4    # "presets":Ljava/util/Collection;, "Ljava/util/Collection<Lmarto/androsdr2/presets/Preset;>;"
    .end local v5    # "size":I
    :catchall_0
    move-exception v6

    monitor-exit v7
    :try_end_2
    .catchall {:try_start_2 .. :try_end_2} :catchall_0

    throw v6

    .line 732
    .restart local v1    # "btns":[Lmarto/tools/gui/SDRPresetButton;
    :catchall_1
    move-exception v6

    :try_start_3
    iget-object v8, p0, Lmarto/androsdr2/SDRTouchMain;->btns_favs:Lmarto/tools/ExpandingArray;

    invoke-virtual {v8}, Lmarto/tools/ExpandingArray;->unlock()V

    throw v6

    .line 759
    .restart local v2    # "i":I
    .restart local v4    # "presets":Ljava/util/Collection;, "Ljava/util/Collection<Lmarto/androsdr2/presets/Preset;>;"
    .restart local v5    # "size":I
    :cond_2
    iget-object v6, p0, Lmarto/androsdr2/SDRTouchMain;->linlay_presetsplace:Landroid/widget/LinearLayout;

    iget-object v8, p0, Lmarto/androsdr2/SDRTouchMain;->btn_add:Landroid/widget/Button;

    invoke-virtual {v6, v8}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;)V

    .line 760
    monitor-exit v7
    :try_end_3
    .catchall {:try_start_3 .. :try_end_3} :catchall_0

    .line 761
    return-void
.end method

.method private exportPresets()V
    .locals 6

    .prologue
    .line 949
    :try_start_0
    new-instance v1, Ljava/io/File;

    invoke-static {}, Landroid/os/Environment;->getExternalStorageDirectory()Ljava/io/File;

    move-result-object v2

    invoke-virtual {v2}, Ljava/io/File;->getCanonicalPath()Ljava/lang/String;

    move-result-object v2

    const-string v3, "SDRTouchPresets.xml"

    invoke-direct {v1, v2, v3}, Ljava/io/File;-><init>(Ljava/lang/String;Ljava/lang/String;)V

    .line 950
    .local v1, "file":Ljava/io/File;
    invoke-virtual {v1}, Ljava/io/File;->exists()Z

    move-result v2

    if-eqz v2, :cond_0

    invoke-virtual {v1}, Ljava/io/File;->delete()Z

    .line 951
    :cond_0
    iget-object v2, p0, Lmarto/androsdr2/SDRTouchMain;->preset_db:Landroid/database/sqlite/SQLiteDatabase;

    invoke-static {v1, v2}, Lmarto/androsdr2/presets/PresetDBManager;->exportToFile(Ljava/io/File;Landroid/database/sqlite/SQLiteDatabase;)V

    .line 952
    const v2, 0x7f07008e

    const/4 v3, 0x1

    new-array v3, v3, [Ljava/lang/Object;

    const/4 v4, 0x0

    invoke-virtual {v1}, Ljava/io/File;->getCanonicalPath()Ljava/lang/String;

    move-result-object v5

    aput-object v5, v3, v4

    invoke-virtual {p0, v2, v3}, Lmarto/androsdr2/SDRTouchMain;->getString(I[Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v2

    const/4 v3, 0x1

    invoke-static {p0, v2, v3}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object v2

    invoke-virtual {v2}, Landroid/widget/Toast;->show()V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 956
    .end local v1    # "file":Ljava/io/File;
    :goto_0
    return-void

    .line 953
    :catch_0
    move-exception v0

    .line 954
    .local v0, "e":Ljava/lang/Exception;
    const-string v2, "Cannot export"

    invoke-virtual {v0}, Ljava/lang/Exception;->getLocalizedMessage()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {p0, v2, v3}, Lmarto/androsdr2/SDRTouchMain;->dialog_showInfo(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_0
.end method

.method private externalFileExists(Ljava/lang/String;)Z
    .locals 3
    .param p1, "filename"    # Ljava/lang/String;

    .prologue
    .line 930
    :try_start_0
    new-instance v1, Ljava/io/File;

    invoke-static {}, Landroid/os/Environment;->getExternalStorageDirectory()Ljava/io/File;

    move-result-object v2

    invoke-virtual {v2}, Ljava/io/File;->getCanonicalPath()Ljava/lang/String;

    move-result-object v2

    invoke-direct {v1, v2, p1}, Ljava/io/File;-><init>(Ljava/lang/String;Ljava/lang/String;)V

    invoke-virtual {v1}, Ljava/io/File;->exists()Z
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    move-result v1

    .line 932
    :goto_0
    return v1

    .line 931
    :catch_0
    move-exception v0

    .line 932
    .local v0, "e":Ljava/lang/Exception;
    const/4 v1, 0x0

    goto :goto_0
.end method

.method private importPresets()V
    .locals 4

    .prologue
    .line 938
    :try_start_0
    new-instance v1, Ljava/io/File;

    invoke-static {}, Landroid/os/Environment;->getExternalStorageDirectory()Ljava/io/File;

    move-result-object v2

    invoke-virtual {v2}, Ljava/io/File;->getCanonicalPath()Ljava/lang/String;

    move-result-object v2

    const-string v3, "SDRTouchPresets.xml"

    invoke-direct {v1, v2, v3}, Ljava/io/File;-><init>(Ljava/lang/String;Ljava/lang/String;)V

    .line 939
    .local v1, "file":Ljava/io/File;
    iget-object v2, p0, Lmarto/androsdr2/SDRTouchMain;->preset_db:Landroid/database/sqlite/SQLiteDatabase;

    invoke-static {v1, v2}, Lmarto/androsdr2/presets/PresetDBManager;->importFromFile(Ljava/io/File;Landroid/database/sqlite/SQLiteDatabase;)V

    .line 940
    const-string v2, "Successfully imported presets"

    const/4 v3, 0x1

    invoke-static {p0, v2, v3}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object v2

    invoke-virtual {v2}, Landroid/widget/Toast;->show()V

    .line 941
    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    invoke-direct {p0, v2}, Lmarto/androsdr2/SDRTouchMain;->createAllButtonsFor(Lmarto/androsdr2/presets/Category;)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 945
    .end local v1    # "file":Ljava/io/File;
    :goto_0
    return-void

    .line 942
    :catch_0
    move-exception v0

    .line 943
    .local v0, "e":Ljava/lang/Exception;
    const-string v2, "Cannot import"

    invoke-virtual {v0}, Ljava/lang/Exception;->getLocalizedMessage()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {p0, v2, v3}, Lmarto/androsdr2/SDRTouchMain;->dialog_showInfo(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_0
.end method

.method private init()V
    .locals 6

    .prologue
    .line 132
    sget-object v1, Lmarto/tools/SharedConstants;->APP_LINKS:Lmarto/tools/FileSyncer;

    invoke-virtual {p0}, Lmarto/androsdr2/SDRTouchMain;->getApplicationContext()Landroid/content/Context;

    move-result-object v2

    invoke-virtual {v1, v2}, Lmarto/tools/FileSyncer;->getLatestFile(Landroid/content/Context;)Ljava/io/InputStream;

    move-result-object v1

    invoke-static {v1}, Lmarto/tools/linking/OtherApps;->fromInputStream(Ljava/io/InputStream;)Lmarto/tools/linking/OtherApps;

    move-result-object v1

    iput-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->appLinkingInfo:Lmarto/tools/linking/OtherApps;

    .line 134
    new-instance v1, Ljava/util/ArrayList;

    invoke-direct {v1}, Ljava/util/ArrayList;-><init>()V

    iput-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->SUPPORTED_MODULATIONS_AND_NAMES:Ljava/util/List;

    .line 136
    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->SUPPORTED_MODULATIONS_AND_NAMES:Ljava/util/List;

    new-instance v2, Landroid/util/Pair;

    new-instance v3, Lmarto/tools/macros/SetModulation;

    iget-object v4, p0, Lmarto/androsdr2/SDRTouchMain;->comm:Lmarto/sdr/javasdr/SDRRadioActivity$SDRCommunicator;

    sget-object v5, Lmarto/sdr/javasdr/SDRRadio$MODULATION;->FM:Lmarto/sdr/javasdr/SDRRadio$MODULATION;

    invoke-direct {v3, v4, v5}, Lmarto/tools/macros/SetModulation;-><init>(Lmarto/tools/MessageClient;Lmarto/sdr/javasdr/SDRRadio$MODULATION;)V

    const v4, 0x7f070097

    invoke-static {v4}, Lmarto/tools/ResourcedStringBuilder;->buildFor(I)Lmarto/tools/ResourcedString;

    move-result-object v4

    invoke-direct {v2, v3, v4}, Landroid/util/Pair;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    invoke-interface {v1, v2}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    .line 137
    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->SUPPORTED_MODULATIONS_AND_NAMES:Ljava/util/List;

    new-instance v2, Landroid/util/Pair;

    new-instance v3, Lmarto/tools/macros/SetModulation;

    iget-object v4, p0, Lmarto/androsdr2/SDRTouchMain;->comm:Lmarto/sdr/javasdr/SDRRadioActivity$SDRCommunicator;

    sget-object v5, Lmarto/sdr/javasdr/SDRRadio$MODULATION;->NFM:Lmarto/sdr/javasdr/SDRRadio$MODULATION;

    invoke-direct {v3, v4, v5}, Lmarto/tools/macros/SetModulation;-><init>(Lmarto/tools/MessageClient;Lmarto/sdr/javasdr/SDRRadio$MODULATION;)V

    const v4, 0x7f070095

    invoke-static {v4}, Lmarto/tools/ResourcedStringBuilder;->buildFor(I)Lmarto/tools/ResourcedString;

    move-result-object v4

    invoke-direct {v2, v3, v4}, Landroid/util/Pair;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    invoke-interface {v1, v2}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    .line 138
    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->SUPPORTED_MODULATIONS_AND_NAMES:Ljava/util/List;

    new-instance v2, Landroid/util/Pair;

    new-instance v3, Lmarto/tools/macros/SetModulation;

    iget-object v4, p0, Lmarto/androsdr2/SDRTouchMain;->comm:Lmarto/sdr/javasdr/SDRRadioActivity$SDRCommunicator;

    sget-object v5, Lmarto/sdr/javasdr/SDRRadio$MODULATION;->AM:Lmarto/sdr/javasdr/SDRRadio$MODULATION;

    invoke-direct {v3, v4, v5}, Lmarto/tools/macros/SetModulation;-><init>(Lmarto/tools/MessageClient;Lmarto/sdr/javasdr/SDRRadio$MODULATION;)V

    const v4, 0x7f070092

    invoke-static {v4}, Lmarto/tools/ResourcedStringBuilder;->buildFor(I)Lmarto/tools/ResourcedString;

    move-result-object v4

    invoke-direct {v2, v3, v4}, Landroid/util/Pair;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    invoke-interface {v1, v2}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    .line 139
    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->SUPPORTED_MODULATIONS_AND_NAMES:Ljava/util/List;

    new-instance v2, Landroid/util/Pair;

    new-instance v3, Lmarto/tools/macros/SetModulation;

    iget-object v4, p0, Lmarto/androsdr2/SDRTouchMain;->comm:Lmarto/sdr/javasdr/SDRRadioActivity$SDRCommunicator;

    sget-object v5, Lmarto/sdr/javasdr/SDRRadio$MODULATION;->LSB:Lmarto/sdr/javasdr/SDRRadio$MODULATION;

    invoke-direct {v3, v4, v5}, Lmarto/tools/macros/SetModulation;-><init>(Lmarto/tools/MessageClient;Lmarto/sdr/javasdr/SDRRadio$MODULATION;)V

    const v4, 0x7f070094

    invoke-static {v4}, Lmarto/tools/ResourcedStringBuilder;->buildFor(I)Lmarto/tools/ResourcedString;

    move-result-object v4

    invoke-direct {v2, v3, v4}, Landroid/util/Pair;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    invoke-interface {v1, v2}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    .line 140
    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->SUPPORTED_MODULATIONS_AND_NAMES:Ljava/util/List;

    new-instance v2, Landroid/util/Pair;

    new-instance v3, Lmarto/tools/macros/SetModulation;

    iget-object v4, p0, Lmarto/androsdr2/SDRTouchMain;->comm:Lmarto/sdr/javasdr/SDRRadioActivity$SDRCommunicator;

    sget-object v5, Lmarto/sdr/javasdr/SDRRadio$MODULATION;->USB:Lmarto/sdr/javasdr/SDRRadio$MODULATION;

    invoke-direct {v3, v4, v5}, Lmarto/tools/macros/SetModulation;-><init>(Lmarto/tools/MessageClient;Lmarto/sdr/javasdr/SDRRadio$MODULATION;)V

    const v4, 0x7f070096

    invoke-static {v4}, Lmarto/tools/ResourcedStringBuilder;->buildFor(I)Lmarto/tools/ResourcedString;

    move-result-object v4

    invoke-direct {v2, v3, v4}, Landroid/util/Pair;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    invoke-interface {v1, v2}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    .line 141
    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->SUPPORTED_MODULATIONS_AND_NAMES:Ljava/util/List;

    new-instance v2, Landroid/util/Pair;

    new-instance v3, Lmarto/tools/macros/SetModulation;

    iget-object v4, p0, Lmarto/androsdr2/SDRTouchMain;->comm:Lmarto/sdr/javasdr/SDRRadioActivity$SDRCommunicator;

    sget-object v5, Lmarto/sdr/javasdr/SDRRadio$MODULATION;->CW:Lmarto/sdr/javasdr/SDRRadio$MODULATION;

    invoke-direct {v3, v4, v5}, Lmarto/tools/macros/SetModulation;-><init>(Lmarto/tools/MessageClient;Lmarto/sdr/javasdr/SDRRadio$MODULATION;)V

    const v4, 0x7f070093

    invoke-static {v4}, Lmarto/tools/ResourcedStringBuilder;->buildFor(I)Lmarto/tools/ResourcedString;

    move-result-object v4

    invoke-direct {v2, v3, v4}, Landroid/util/Pair;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    invoke-interface {v1, v2}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    .line 143
    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->appLinkingInfo:Lmarto/tools/linking/OtherApps;

    sget-object v2, Lmarto/tools/linking/OtherApps$App;->AERIAL_TV:Lmarto/tools/linking/OtherApps$App;

    invoke-virtual {v1, v2}, Lmarto/tools/linking/OtherApps;->isKnown(Lmarto/tools/linking/OtherApps$App;)Z

    move-result v1

    if-eqz v1, :cond_0

    .line 144
    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->SUPPORTED_MODULATIONS_AND_NAMES:Ljava/util/List;

    new-instance v2, Landroid/util/Pair;

    new-instance v3, Lmarto/tools/macros/StartOrInstallApp;

    sget-object v4, Lmarto/tools/linking/OtherApps$App;->AERIAL_TV:Lmarto/tools/linking/OtherApps$App;

    iget-object v5, p0, Lmarto/androsdr2/SDRTouchMain;->appLinkingInfo:Lmarto/tools/linking/OtherApps;

    invoke-direct {v3, v4, v5, p0}, Lmarto/tools/macros/StartOrInstallApp;-><init>(Lmarto/tools/linking/OtherApps$App;Lmarto/tools/linking/OtherApps;Landroid/content/Context;)V

    .line 145
    invoke-static {v3}, Lmarto/tools/macros/Chain;->exec(Ljava/lang/Runnable;)Lmarto/tools/macros/Chain;

    move-result-object v3

    iget-object v4, p0, Lmarto/androsdr2/SDRTouchMain;->actionShutDown:Lmarto/tools/macros/ShutDown;

    invoke-virtual {v3, v4}, Lmarto/tools/macros/Chain;->then(Ljava/lang/Runnable;)Lmarto/tools/macros/Chain;

    move-result-object v3

    const v4, 0x7f07010a

    invoke-static {v4}, Lmarto/tools/ResourcedStringBuilder;->buildFor(I)Lmarto/tools/ResourcedString;

    move-result-object v4

    invoke-direct {v2, v3, v4}, Landroid/util/Pair;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 144
    invoke-interface {v1, v2}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    .line 149
    :cond_0
    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->SUPPORTED_MODULATIONS_AND_NAMES:Ljava/util/List;

    invoke-interface {v1}, Ljava/util/List;->size()I

    move-result v1

    new-array v1, v1, [Lmarto/tools/ResourcedString;

    iput-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->MODULATION_NAMES:[Lmarto/tools/ResourcedString;

    .line 150
    const/4 v0, 0x0

    .local v0, "i":I
    :goto_0
    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->MODULATION_NAMES:[Lmarto/tools/ResourcedString;

    array-length v1, v1

    if-ge v0, v1, :cond_1

    .line 151
    iget-object v2, p0, Lmarto/androsdr2/SDRTouchMain;->MODULATION_NAMES:[Lmarto/tools/ResourcedString;

    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->SUPPORTED_MODULATIONS_AND_NAMES:Ljava/util/List;

    invoke-interface {v1, v0}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Landroid/util/Pair;

    iget-object v1, v1, Landroid/util/Pair;->second:Ljava/lang/Object;

    check-cast v1, Lmarto/tools/ResourcedString;

    aput-object v1, v2, v0

    .line 150
    add-int/lit8 v0, v0, 0x1

    goto :goto_0

    .line 153
    :cond_1
    return-void
.end method

.method private loadPrefs()V
    .locals 4

    .prologue
    .line 298
    const-string v2, "SDRTouchMain"

    const/4 v3, 0x0

    invoke-virtual {p0, v2, v3}, Lmarto/androsdr2/SDRTouchMain;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;

    move-result-object v0

    .line 301
    .local v0, "settings":Landroid/content/SharedPreferences;
    :try_start_0
    const-string v2, "remote"

    iget-object v3, p0, Lmarto/androsdr2/SDRTouchMain;->remote:Ljava/lang/String;

    invoke-interface {v0, v2, v3}, Landroid/content/SharedPreferences;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    iput-object v2, p0, Lmarto/androsdr2/SDRTouchMain;->remote:Ljava/lang/String;

    .line 302
    const-string v2, "firstrun"

    const/4 v3, 0x1

    invoke-interface {v0, v2, v3}, Landroid/content/SharedPreferences;->getBoolean(Ljava/lang/String;Z)Z

    move-result v2

    iput-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->firstrun:Z

    .line 303
    const-string v2, "category"

    const/4 v3, 0x0

    invoke-interface {v0, v2, v3}, Landroid/content/SharedPreferences;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    iput-object v2, p0, Lmarto/androsdr2/SDRTouchMain;->lastCatName:Ljava/lang/String;
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0

    .line 308
    :goto_0
    return-void

    .line 304
    :catch_0
    move-exception v1

    .line 305
    .local v1, "t":Ljava/lang/Throwable;
    invoke-virtual {v1}, Ljava/lang/Throwable;->printStackTrace()V

    goto :goto_0
.end method

.method private onRecordButtonClicked()V
    .locals 3

    .prologue
    .line 472
    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->btn_rec:Landroid/widget/ToggleButton;

    const/4 v2, 0x0

    invoke-virtual {v1, v2}, Landroid/widget/ToggleButton;->setChecked(Z)V

    .line 473
    new-instance v0, Lmarto/androsdr2/SDRTouchMain$3;

    invoke-direct {v0, p0}, Lmarto/androsdr2/SDRTouchMain$3;-><init>(Lmarto/androsdr2/SDRTouchMain;)V

    .line 486
    .local v0, "showRecordingDialog":Ljava/lang/Runnable;
    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->permissionObtainer:Lmarto/sdr/javasdr/RuntimePermissionObtainer;

    const-string v2, "android.permission.WRITE_EXTERNAL_STORAGE"

    invoke-virtual {v1, v2, v0}, Lmarto/sdr/javasdr/RuntimePermissionObtainer;->runIfPermissionAvailable(Ljava/lang/String;Ljava/lang/Runnable;)V

    .line 487
    return-void
.end method

.method private onScanButtonClicked()V
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lmarto/sdr/javasdr/exceptions/SDRException;
        }
    .end annotation

    .prologue
    .line 464
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_scan:Landroid/widget/ToggleButton;

    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->scanner:Lmarto/androsdr2/presets/PresetScanner;

    invoke-virtual {v1}, Lmarto/androsdr2/presets/PresetScanner;->isScanning()Z

    move-result v1

    invoke-virtual {v0, v1}, Landroid/widget/ToggleButton;->setChecked(Z)V

    .line 465
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->scanner:Lmarto/androsdr2/presets/PresetScanner;

    invoke-virtual {v0}, Lmarto/androsdr2/presets/PresetScanner;->isScanning()Z

    move-result v0

    if-eqz v0, :cond_0

    .line 466
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->scanner:Lmarto/androsdr2/presets/PresetScanner;

    invoke-virtual {v0}, Lmarto/androsdr2/presets/PresetScanner;->stopScan()V

    .line 469
    :goto_0
    return-void

    .line 468
    :cond_0
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->scanner:Lmarto/androsdr2/presets/PresetScanner;

    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->btns_favs:Lmarto/tools/ExpandingArray;

    invoke-virtual {v0, v1}, Lmarto/androsdr2/presets/PresetScanner;->startScan(Lmarto/tools/ExpandingArray;)V

    goto :goto_0
.end method

.method private open_dialog_clicked(I)V
    .locals 3
    .param p1, "id"    # I

    .prologue
    .line 685
    packed-switch p1, :pswitch_data_0

    .line 693
    :goto_0
    return-void

    .line 687
    :pswitch_0
    invoke-direct {p0}, Lmarto/androsdr2/SDRTouchMain;->open_local_file()V

    goto :goto_0

    .line 690
    :pswitch_1
    const/4 v0, 0x5

    const v1, 0x7f07009e

    invoke-virtual {p0, v1}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v1

    iget-object v2, p0, Lmarto/androsdr2/SDRTouchMain;->remote:Ljava/lang/String;

    invoke-virtual {p0, v0, v1, v2}, Lmarto/androsdr2/SDRTouchMain;->dialog_showTextInput(ILjava/lang/String;Ljava/lang/String;)V

    goto :goto_0

    .line 685
    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_1
    .end packed-switch
.end method

.method private open_local_file()V
    .locals 5
    .annotation build Landroid/annotation/SuppressLint;
        value = {
            "InlinedApi"
        }
    .end annotation

    .prologue
    .line 665
    new-instance v1, Landroid/content/Intent;

    const-string v2, "android.intent.action.GET_CONTENT"

    invoke-direct {v1, v2}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 666
    .local v1, "intent":Landroid/content/Intent;
    const-string v2, "*/*"

    invoke-virtual {v1, v2}, Landroid/content/Intent;->setType(Ljava/lang/String;)Landroid/content/Intent;

    .line 667
    const-string v2, "android.intent.category.OPENABLE"

    invoke-virtual {v1, v2}, Landroid/content/Intent;->addCategory(Ljava/lang/String;)Landroid/content/Intent;

    .line 671
    :try_start_0
    iget-object v2, p0, Lmarto/androsdr2/SDRTouchMain;->activityOpener:Lmarto/tools/ActivityOpener;

    const v3, 0x7f07009b

    invoke-virtual {p0, v3}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v3

    invoke-static {v1, v3}, Landroid/content/Intent;->createChooser(Landroid/content/Intent;Ljava/lang/CharSequence;)Landroid/content/Intent;

    move-result-object v3

    new-instance v4, Lmarto/androsdr2/SDRTouchMain$9;

    invoke-direct {v4, p0}, Lmarto/androsdr2/SDRTouchMain$9;-><init>(Lmarto/androsdr2/SDRTouchMain;)V

    invoke-virtual {v2, p0, v3, v4}, Lmarto/tools/ActivityOpener;->launch(Landroid/app/Activity;Landroid/content/Intent;Lmarto/tools/ActivityOpener$Callback;)V
    :try_end_0
    .catch Landroid/content/ActivityNotFoundException; {:try_start_0 .. :try_end_0} :catch_0

    .line 682
    :goto_0
    return-void

    .line 679
    :catch_0
    move-exception v0

    .line 680
    .local v0, "ex":Landroid/content/ActivityNotFoundException;
    const v2, 0x7f07009a

    invoke-virtual {p0, v2}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v2

    const v3, 0x7f070099

    invoke-virtual {p0, v3}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {p0, v2, v3}, Lmarto/androsdr2/SDRTouchMain;->dialog_showInfo(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_0
.end method

.method private preset_menu_clicked(I)V
    .locals 5
    .param p1, "id"    # I

    .prologue
    .line 764
    packed-switch p1, :pswitch_data_0

    .line 793
    :goto_0
    return-void

    .line 766
    :pswitch_0
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    if-eqz v0, :cond_0

    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->latest_preset:Lmarto/androsdr2/presets/Preset;

    if-nez v0, :cond_1

    .line 767
    :cond_0
    new-instance v0, Ljava/lang/RuntimeException;

    const-string v1, "Cannot replace the preset."

    invoke-direct {v0, v1}, Ljava/lang/RuntimeException;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->onException(Ljava/lang/Exception;)V

    goto :goto_0

    .line 770
    :cond_1
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->latest_preset:Lmarto/androsdr2/presets/Preset;

    sget-object v1, Lmarto/androsdr2/SDRTouchMain;->currPreset:Lmarto/androsdr2/presets/Preset;

    iget v1, v1, Lmarto/androsdr2/presets/Preset;->id:I

    iput v1, v0, Lmarto/androsdr2/presets/Preset;->id:I

    .line 771
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->latest_preset:Lmarto/androsdr2/presets/Preset;

    sget-object v1, Lmarto/androsdr2/SDRTouchMain;->currPreset:Lmarto/androsdr2/presets/Preset;

    iget-object v1, v1, Lmarto/androsdr2/presets/Preset;->name:Ljava/lang/String;

    iput-object v1, v0, Lmarto/androsdr2/presets/Preset;->name:Ljava/lang/String;

    .line 772
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->latest_preset:Lmarto/androsdr2/presets/Preset;

    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->preset_db:Landroid/database/sqlite/SQLiteDatabase;

    invoke-static {v0, v1}, Lmarto/androsdr2/presets/PresetDBManager;->addOrEditPreset(Lmarto/androsdr2/presets/Preset;Landroid/database/sqlite/SQLiteDatabase;)V

    .line 773
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    invoke-direct {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->createAllButtonsFor(Lmarto/androsdr2/presets/Category;)V

    goto :goto_0

    .line 776
    :pswitch_1
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currPreset:Lmarto/androsdr2/presets/Preset;

    if-nez v0, :cond_2

    .line 777
    new-instance v0, Ljava/lang/RuntimeException;

    const-string v1, "Cannot rename the preset."

    invoke-direct {v0, v1}, Ljava/lang/RuntimeException;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->onException(Ljava/lang/Exception;)V

    goto :goto_0

    .line 780
    :cond_2
    const/4 v0, 0x3

    const v1, 0x7f0700cb

    invoke-virtual {p0, v1}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v1

    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->currPreset:Lmarto/androsdr2/presets/Preset;

    iget-object v2, v2, Lmarto/androsdr2/presets/Preset;->name:Ljava/lang/String;

    invoke-virtual {p0, v0, v1, v2}, Lmarto/androsdr2/SDRTouchMain;->dialog_showTextInput(ILjava/lang/String;Ljava/lang/String;)V

    goto :goto_0

    .line 783
    :pswitch_2
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currPreset:Lmarto/androsdr2/presets/Preset;

    if-nez v0, :cond_3

    .line 784
    new-instance v0, Ljava/lang/RuntimeException;

    const-string v1, "Cannot delete the preset."

    invoke-direct {v0, v1}, Ljava/lang/RuntimeException;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->onException(Ljava/lang/Exception;)V

    goto :goto_0

    .line 787
    :cond_3
    const/4 v0, 0x2

    const v1, 0x7f0700ca

    const/4 v2, 0x1

    new-array v2, v2, [Ljava/lang/Object;

    const/4 v3, 0x0

    sget-object v4, Lmarto/androsdr2/SDRTouchMain;->currPreset:Lmarto/androsdr2/presets/Preset;

    iget-object v4, v4, Lmarto/androsdr2/presets/Preset;->name:Ljava/lang/String;

    aput-object v4, v2, v3

    invoke-virtual {p0, v1, v2}, Lmarto/androsdr2/SDRTouchMain;->getString(I[Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {p0, v0, v1}, Lmarto/androsdr2/SDRTouchMain;->dialog_showYesNo(ILjava/lang/String;)V

    goto :goto_0

    .line 764
    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_1
        :pswitch_2
    .end packed-switch
.end method

.method private recalcActivePresetButton()V
    .locals 6

    .prologue
    .line 698
    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->btns_favs_sparse:Landroid/support/v4/util/SparseArrayCompat;

    iget-wide v2, p0, Lmarto/androsdr2/SDRTouchMain;->mCentFreq:J

    iget-wide v4, p0, Lmarto/androsdr2/SDRTouchMain;->mVFOFreq:J

    add-long/2addr v2, v4

    const-wide/16 v4, 0x3e8

    div-long/2addr v2, v4

    long-to-int v2, v2

    invoke-virtual {v1, v2}, Landroid/support/v4/util/SparseArrayCompat;->get(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lmarto/tools/gui/SDRPresetButton;

    .line 699
    .local v0, "btn":Lmarto/tools/gui/SDRPresetButton;
    if-nez v0, :cond_0

    sget-boolean v1, Lmarto/androsdr2/SDRTouchMain;->forcePresetButtonsActiveStateRecheck:Z

    if-eqz v1, :cond_1

    .line 700
    :cond_0
    if-eqz v0, :cond_2

    const/4 v1, 0x1

    :goto_0
    sput-boolean v1, Lmarto/androsdr2/SDRTouchMain;->forcePresetButtonsActiveStateRecheck:Z

    .line 701
    new-instance v1, Lmarto/androsdr2/SDRTouchMain$10;

    invoke-direct {v1, p0, v0}, Lmarto/androsdr2/SDRTouchMain$10;-><init>(Lmarto/androsdr2/SDRTouchMain;Lmarto/tools/gui/SDRPresetButton;)V

    invoke-virtual {p0, v1}, Lmarto/androsdr2/SDRTouchMain;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 718
    :cond_1
    return-void

    .line 700
    :cond_2
    const/4 v1, 0x0

    goto :goto_0
.end method

.method private remoteStart(Landroid/net/Uri;)V
    .locals 1
    .param p1, "uri"    # Landroid/net/Uri;

    .prologue
    .line 395
    const/4 v0, 0x0

    invoke-direct {p0, p1, v0}, Lmarto/androsdr2/SDRTouchMain;->remoteStart(Landroid/net/Uri;Z)V

    .line 396
    return-void
.end method

.method private remoteStart(Landroid/net/Uri;Z)V
    .locals 8
    .param p1, "uri"    # Landroid/net/Uri;
    .param p2, "isFromFileForSure"    # Z

    .prologue
    .line 446
    :try_start_0
    invoke-direct {p0, p1}, Lmarto/androsdr2/SDRTouchMain;->tryStartingFromFileScheme(Landroid/net/Uri;)Z

    move-result v2

    if-eqz v2, :cond_1

    .line 461
    :cond_0
    :goto_0
    return-void

    .line 447
    :cond_1
    invoke-direct {p0, p1}, Lmarto/androsdr2/SDRTouchMain;->tryStartingFromContentScheme(Landroid/net/Uri;)Z

    move-result v2

    if-nez v2, :cond_0

    .line 448
    invoke-direct {p0, p1}, Lmarto/androsdr2/SDRTouchMain;->tryStartingFromAudioContent(Landroid/net/Uri;)Z

    move-result v2

    if-nez v2, :cond_0

    .line 449
    if-eqz p2, :cond_2

    new-instance v2, Lmarto/sdr/javasdr/exceptions/SDRExceptionWarning;

    const v3, 0x7f070015

    const/4 v4, 0x1

    new-array v4, v4, [Ljava/lang/Object;

    const/4 v5, 0x0

    new-instance v6, Ljava/io/File;

    invoke-virtual {p1}, Landroid/net/Uri;->getPath()Ljava/lang/String;

    move-result-object v7

    invoke-direct {v6, v7}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    invoke-virtual {v6}, Ljava/io/File;->getName()Ljava/lang/String;

    move-result-object v6

    aput-object v6, v4, v5

    invoke-virtual {p0, v3, v4}, Lmarto/androsdr2/SDRTouchMain;->getString(I[Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v3

    invoke-direct {v2, v3}, Lmarto/sdr/javasdr/exceptions/SDRExceptionWarning;-><init>(Ljava/lang/String;)V

    throw v2
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 458
    :catch_0
    move-exception v0

    .line 459
    .local v0, "e":Ljava/lang/Exception;
    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->onException(Ljava/lang/Exception;)V

    goto :goto_0

    .line 452
    .end local v0    # "e":Ljava/lang/Exception;
    :cond_2
    :try_start_1
    invoke-virtual {p1}, Landroid/net/Uri;->getPort()I

    move-result v1

    .line 453
    .local v1, "port_number":I
    const/4 v2, -0x1

    if-ne v1, v2, :cond_3

    const/16 v1, 0x4d2

    .line 454
    :cond_3
    if-ltz v1, :cond_4

    const v2, 0xffff

    if-le v1, v2, :cond_5

    .line 455
    :cond_4
    new-instance v2, Lmarto/sdr/javasdr/exceptions/SDRExceptionWarning;

    const v3, 0x7f0700ae

    invoke-virtual {p0, v3}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v3

    invoke-direct {v2, v3}, Lmarto/sdr/javasdr/exceptions/SDRExceptionWarning;-><init>(Ljava/lang/String;)V

    throw v2

    .line 457
    :cond_5
    invoke-virtual {p1}, Landroid/net/Uri;->getHost()Ljava/lang/String;

    move-result-object v2

    const/4 v3, 0x0

    invoke-virtual {p0, v2, v1, v3}, Lmarto/androsdr2/SDRTouchMain;->sdrStartFromIP(Ljava/lang/String;I[I)V
    :try_end_1
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_1} :catch_0

    goto :goto_0
.end method

.method private storePrefs()V
    .locals 4

    .prologue
    .line 311
    const-string v2, "SDRTouchMain"

    const/4 v3, 0x0

    invoke-virtual {p0, v2, v3}, Lmarto/androsdr2/SDRTouchMain;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;

    move-result-object v1

    .line 312
    .local v1, "settings":Landroid/content/SharedPreferences;
    invoke-interface {v1}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;

    move-result-object v0

    .line 314
    .local v0, "editor":Landroid/content/SharedPreferences$Editor;
    const-string v2, "firstrun"

    iget-boolean v3, p0, Lmarto/androsdr2/SDRTouchMain;->firstrun:Z

    invoke-interface {v0, v2, v3}, Landroid/content/SharedPreferences$Editor;->putBoolean(Ljava/lang/String;Z)Landroid/content/SharedPreferences$Editor;

    .line 315
    const-string v2, "remote"

    iget-object v3, p0, Lmarto/androsdr2/SDRTouchMain;->remote:Ljava/lang/String;

    invoke-interface {v0, v2, v3}, Landroid/content/SharedPreferences$Editor;->putString(Ljava/lang/String;Ljava/lang/String;)Landroid/content/SharedPreferences$Editor;

    .line 316
    sget-object v2, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    if-eqz v2, :cond_0

    const-string v2, "category"

    sget-object v3, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    iget-object v3, v3, Lmarto/androsdr2/presets/Category;->name:Ljava/lang/String;

    invoke-interface {v0, v2, v3}, Landroid/content/SharedPreferences$Editor;->putString(Ljava/lang/String;Ljava/lang/String;)Landroid/content/SharedPreferences$Editor;

    .line 318
    :cond_0
    invoke-interface {v0}, Landroid/content/SharedPreferences$Editor;->commit()Z

    .line 319
    return-void
.end method

.method private tryStartingFromAudioContent(Landroid/net/Uri;)Z
    .locals 12
    .param p1, "uri"    # Landroid/net/Uri;
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .prologue
    const/4 v11, 0x1

    const/4 v3, 0x0

    const/4 v10, 0x0

    .line 424
    new-array v2, v11, [Ljava/lang/String;

    const-string v0, "_data"

    aput-object v0, v2, v10

    .line 425
    .local v2, "projection":[Ljava/lang/String;
    invoke-virtual {p0}, Lmarto/androsdr2/SDRTouchMain;->getContentResolver()Landroid/content/ContentResolver;

    move-result-object v0

    move-object v1, p1

    move-object v4, v3

    move-object v5, v3

    invoke-virtual/range {v0 .. v5}, Landroid/content/ContentResolver;->query(Landroid/net/Uri;[Ljava/lang/String;Ljava/lang/String;[Ljava/lang/String;Ljava/lang/String;)Landroid/database/Cursor;

    move-result-object v7

    .line 426
    .local v7, "cursor":Landroid/database/Cursor;
    if-nez v7, :cond_0

    move v0, v10

    .line 439
    :goto_0
    return v0

    .line 428
    :cond_0
    const-string v0, "_data"

    invoke-interface {v7, v0}, Landroid/database/Cursor;->getColumnIndexOrThrow(Ljava/lang/String;)I

    move-result v6

    .line 429
    .local v6, "column_index":I
    invoke-interface {v7}, Landroid/database/Cursor;->moveToFirst()Z

    .line 430
    invoke-interface {v7, v6}, Landroid/database/Cursor;->getString(I)Ljava/lang/String;

    move-result-object v9

    .line 431
    .local v9, "filePath":Ljava/lang/String;
    invoke-interface {v7}, Landroid/database/Cursor;->close()V

    .line 433
    if-nez v9, :cond_1

    move v0, v10

    goto :goto_0

    .line 435
    :cond_1
    new-instance v8, Ljava/io/File;

    invoke-direct {v8, v9}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 436
    .local v8, "file":Ljava/io/File;
    invoke-virtual {v8}, Ljava/io/File;->exists()Z

    move-result v0

    if-nez v0, :cond_2

    move v0, v10

    goto :goto_0

    .line 438
    :cond_2
    invoke-virtual {p0, v8}, Lmarto/androsdr2/SDRTouchMain;->sdrStartFromFile(Ljava/io/File;)V

    move v0, v11

    .line 439
    goto :goto_0
.end method

.method private tryStartingFromContentScheme(Landroid/net/Uri;)Z
    .locals 7
    .param p1, "uri"    # Landroid/net/Uri;
    .annotation build Landroid/annotation/SuppressLint;
        value = {
            "NewApi"
        }
    .end annotation

    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .prologue
    const/4 v4, 0x1

    const/4 v3, 0x0

    .line 407
    sget v5, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v6, 0x13

    if-ge v5, v6, :cond_1

    .line 420
    :cond_0
    :goto_0
    return v3

    .line 408
    :cond_1
    invoke-static {p0, p1}, Landroid/provider/DocumentsContract;->isDocumentUri(Landroid/content/Context;Landroid/net/Uri;)Z

    move-result v5

    if-eqz v5, :cond_0

    .line 409
    const-string v5, "com.android.externalstorage.documents"

    invoke-virtual {p1}, Landroid/net/Uri;->getAuthority()Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v5, v6}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v5

    if-eqz v5, :cond_0

    .line 411
    invoke-static {p1}, Landroid/provider/DocumentsContract;->getDocumentId(Landroid/net/Uri;)Ljava/lang/String;

    move-result-object v0

    .line 412
    .local v0, "docId":Ljava/lang/String;
    const-string v5, ":"

    invoke-virtual {v0, v5}, Ljava/lang/String;->split(Ljava/lang/String;)[Ljava/lang/String;

    move-result-object v1

    .line 413
    .local v1, "split":[Ljava/lang/String;
    aget-object v2, v1, v3

    .line 415
    .local v2, "type":Ljava/lang/String;
    const-string v5, "primary"

    invoke-virtual {v5, v2}, Ljava/lang/String;->equalsIgnoreCase(Ljava/lang/String;)Z

    move-result v5

    if-eqz v5, :cond_0

    .line 416
    new-instance v3, Ljava/io/File;

    invoke-static {}, Landroid/os/Environment;->getExternalStorageDirectory()Ljava/io/File;

    move-result-object v5

    aget-object v6, v1, v4

    invoke-direct {v3, v5, v6}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    invoke-virtual {p0, v3}, Lmarto/androsdr2/SDRTouchMain;->sdrStartFromFile(Ljava/io/File;)V

    move v3, v4

    .line 417
    goto :goto_0
.end method

.method private tryStartingFromFileScheme(Landroid/net/Uri;)Z
    .locals 2
    .param p1, "uri"    # Landroid/net/Uri;
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .prologue
    .line 399
    invoke-virtual {p1}, Landroid/net/Uri;->getScheme()Ljava/lang/String;

    move-result-object v0

    const-string v1, "file"

    invoke-virtual {v0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_0

    const/4 v0, 0x0

    .line 402
    :goto_0
    return v0

    .line 401
    :cond_0
    new-instance v0, Ljava/io/File;

    invoke-virtual {p1}, Landroid/net/Uri;->getPath()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->sdrStartFromFile(Ljava/io/File;)V

    .line 402
    const/4 v0, 0x1

    goto :goto_0
.end method


# virtual methods
.method public OnAudioGain(I)V
    .locals 4
    .param p1, "audio_gain"    # I

    .prologue
    .line 391
    sget-object v0, Lmarto/sdr/javasdr/SDRMessageFromClient;->SET_AUDIO_BOOST:Lmarto/sdr/javasdr/SDRMessageFromClient;

    int-to-long v2, p1

    invoke-virtual {p0, v0, v2, v3}, Lmarto/androsdr2/SDRTouchMain;->sdrSendMessageToServer(Lmarto/sdr/javasdr/SDRMessageFromClient;J)V

    .line 392
    return-void
.end method

.method public OnFrequencyEntered(ILjava/lang/String;I)V
    .locals 10
    .param p1, "id"    # I
    .param p2, "text"    # Ljava/lang/String;
    .param p3, "multiplier"    # I

    .prologue
    .line 492
    const-wide/16 v8, 0x0

    .line 494
    .local v8, "freq":J
    :try_start_0
    invoke-static {p2}, Ljava/lang/Double;->parseDouble(Ljava/lang/String;)D

    move-result-wide v0

    int-to-double v2, p3

    mul-double/2addr v0, v2

    invoke-static {v0, v1}, Ljava/lang/Math;->round(D)J
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    move-result-wide v8

    .line 499
    :goto_0
    packed-switch p1, :pswitch_data_0

    .line 510
    :goto_1
    return-void

    .line 495
    :catch_0
    move-exception v6

    .line 496
    .local v6, "e":Ljava/lang/Exception;
    const v0, 0x7f0700a6

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->onWarning(I)V

    goto :goto_0

    .line 501
    .end local v6    # "e":Ljava/lang/Exception;
    :pswitch_0
    sget-object v1, Lmarto/sdr/javasdr/SDRMessageFromClient;->SET_CENTRAL_FREQ:Lmarto/sdr/javasdr/SDRMessageFromClient;

    iget-wide v2, p0, Lmarto/androsdr2/SDRTouchMain;->mVFOFreq:J

    sub-long v2, v8, v2

    const-wide/16 v4, 0x1

    move-object v0, p0

    invoke-virtual/range {v0 .. v5}, Lmarto/androsdr2/SDRTouchMain;->sdrSendMessageToServer(Lmarto/sdr/javasdr/SDRMessageFromClient;JJ)V

    goto :goto_1

    .line 504
    :pswitch_1
    sget-object v0, Lmarto/sdr/javasdr/SDRMessageFromClient;->SET_OFFSET:Lmarto/sdr/javasdr/SDRMessageFromClient;

    invoke-virtual {p0, v0, v8, v9}, Lmarto/androsdr2/SDRTouchMain;->sdrSendMessageToServer(Lmarto/sdr/javasdr/SDRMessageFromClient;J)V

    goto :goto_1

    .line 499
    nop

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_1
    .end packed-switch
.end method

.method public OnGainManualModeSet(Z)V
    .locals 3
    .param p1, "gain_mode"    # Z

    .prologue
    .line 386
    sget-object v2, Lmarto/sdr/javasdr/SDRMessageFromClient;->SET_GAIN_MANUAL:Lmarto/sdr/javasdr/SDRMessageFromClient;

    if-eqz p1, :cond_0

    const-wide/16 v0, 0x1

    :goto_0
    invoke-virtual {p0, v2, v0, v1}, Lmarto/androsdr2/SDRTouchMain;->sdrSendMessageToServer(Lmarto/sdr/javasdr/SDRMessageFromClient;J)V

    .line 387
    return-void

    .line 386
    :cond_0
    const-wide/16 v0, 0x0

    goto :goto_0
.end method

.method public OnGainSet(I)V
    .locals 4
    .param p1, "gain"    # I

    .prologue
    .line 381
    sget-object v0, Lmarto/sdr/javasdr/SDRMessageFromClient;->SET_GAIN:Lmarto/sdr/javasdr/SDRMessageFromClient;

    int-to-long v2, p1

    invoke-virtual {p0, v0, v2, v3}, Lmarto/androsdr2/SDRTouchMain;->sdrSendMessageToServer(Lmarto/sdr/javasdr/SDRMessageFromClient;J)V

    .line 382
    return-void
.end method

.method public OnPPMset(I)V
    .locals 4
    .param p1, "ppm"    # I

    .prologue
    .line 376
    sget-object v0, Lmarto/sdr/javasdr/SDRMessageFromClient;->SET_PPM:Lmarto/sdr/javasdr/SDRMessageFromClient;

    int-to-long v2, p1

    invoke-virtual {p0, v0, v2, v3}, Lmarto/androsdr2/SDRTouchMain;->sdrSendMessageToServer(Lmarto/sdr/javasdr/SDRMessageFromClient;J)V

    .line 377
    return-void
.end method

.method protected getMessages()[Lmarto/sdr/javasdr/SDRMessageFromServer;
    .locals 1

    .prologue
    .line 659
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->messages:[Lmarto/sdr/javasdr/SDRMessageFromServer;

    return-object v0
.end method

.method public onClick(Landroid/view/View;)V
    .locals 10
    .param p1, "v"    # Landroid/view/View;

    .prologue
    .line 325
    :try_start_0
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_onoff:Landroid/widget/Button;

    if-ne p1, v0, :cond_2

    .line 326
    iget-boolean v0, p0, Lmarto/androsdr2/SDRTouchMain;->on:Z

    if-nez v0, :cond_1

    .line 327
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_onoff:Landroid/widget/Button;

    check-cast v0, Landroid/widget/ToggleButton;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Landroid/widget/ToggleButton;->setChecked(Z)V

    .line 328
    invoke-virtual {p0}, Lmarto/androsdr2/SDRTouchMain;->sdrStartFromDriver()V

    .line 372
    :cond_0
    :goto_0
    return-void

    .line 330
    :cond_1
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->actionShutDown:Lmarto/tools/macros/ShutDown;

    invoke-virtual {v0}, Lmarto/tools/macros/ShutDown;->run()V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 369
    :catch_0
    move-exception v7

    .line 370
    .local v7, "e":Ljava/lang/Exception;
    invoke-virtual {p0, v7}, Lmarto/androsdr2/SDRTouchMain;->onException(Ljava/lang/Exception;)V

    goto :goto_0

    .line 332
    .end local v7    # "e":Ljava/lang/Exception;
    :cond_2
    :try_start_1
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_show_favs:Landroid/widget/Button;

    if-ne p1, v0, :cond_3

    .line 333
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_show_favs:Landroid/widget/Button;

    const/16 v1, 0x8

    invoke-virtual {v0, v1}, Landroid/widget/Button;->setVisibility(I)V

    .line 334
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->linlay_favs:Landroid/widget/LinearLayout;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->setVisibility(I)V

    goto :goto_0

    .line 335
    :cond_3
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_show_menu:Landroid/widget/Button;

    if-ne p1, v0, :cond_4

    .line 336
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_show_menu:Landroid/widget/Button;

    const/16 v1, 0x8

    invoke-virtual {v0, v1}, Landroid/widget/Button;->setVisibility(I)V

    .line 337
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->linlay_menu:Landroid/widget/LinearLayout;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->setVisibility(I)V

    goto :goto_0

    .line 338
    :cond_4
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_hide_favs:Landroid/widget/Button;

    if-ne p1, v0, :cond_5

    .line 339
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_show_favs:Landroid/widget/Button;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Landroid/widget/Button;->setVisibility(I)V

    .line 340
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->linlay_favs:Landroid/widget/LinearLayout;

    const/16 v1, 0x8

    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->setVisibility(I)V

    goto :goto_0

    .line 341
    :cond_5
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_hide_menu:Landroid/widget/Button;

    if-ne p1, v0, :cond_6

    .line 342
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_show_menu:Landroid/widget/Button;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Landroid/widget/Button;->setVisibility(I)V

    .line 343
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->linlay_menu:Landroid/widget/LinearLayout;

    const/16 v1, 0x8

    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->setVisibility(I)V

    goto :goto_0

    .line 344
    :cond_6
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_modulation:Landroid/widget/Button;

    if-ne p1, v0, :cond_7

    .line 345
    const/4 v0, 0x1

    const v1, 0x7f070098

    invoke-virtual {p0, v1}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v1

    iget-object v2, p0, Lmarto/androsdr2/SDRTouchMain;->MODULATION_NAMES:[Lmarto/tools/ResourcedString;

    invoke-virtual {p0, v0, v1, v2}, Lmarto/androsdr2/SDRTouchMain;->dialog_showItemsChooser(ILjava/lang/String;[Ljava/lang/Object;)V

    goto :goto_0

    .line 346
    :cond_7
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_add:Landroid/widget/Button;

    if-ne p1, v0, :cond_8

    .line 347
    invoke-direct {p0}, Lmarto/androsdr2/SDRTouchMain;->btn_addClicked()V

    goto :goto_0

    .line 348
    :cond_8
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_cat:Landroid/widget/Button;

    if-ne p1, v0, :cond_9

    .line 349
    invoke-direct {p0}, Lmarto/androsdr2/SDRTouchMain;->btn_catClicked()V

    goto :goto_0

    .line 350
    :cond_9
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_jump:Landroid/widget/Button;

    if-ne p1, v0, :cond_a

    .line 351
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->dialogDisplayer:Lmarto/tools/gui/menus/DialogFragmentDisplayer;

    const/4 v1, 0x0

    const v2, 0x7f070091

    invoke-virtual {p0, v2}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v2

    iget-wide v4, p0, Lmarto/androsdr2/SDRTouchMain;->mCentFreq:J

    iget-wide v8, p0, Lmarto/androsdr2/SDRTouchMain;->mVFOFreq:J

    add-long/2addr v4, v8

    const/4 v3, 0x0

    invoke-static {v1, v2, v4, v5, v3}, Lmarto/tools/gui/dialogs/DialogFreqChooser;->create(ILjava/lang/String;JZ)Landroid/support/v4/app/DialogFragment;

    move-result-object v1

    invoke-virtual {v0, v1}, Lmarto/tools/gui/menus/DialogFragmentDisplayer;->dialog_showOneOnlyCustom(Landroid/support/v4/app/DialogFragment;)V

    goto/16 :goto_0

    .line 352
    :cond_a
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_scan:Landroid/widget/ToggleButton;

    if-ne p1, v0, :cond_b

    .line 353
    invoke-direct {p0}, Lmarto/androsdr2/SDRTouchMain;->onScanButtonClicked()V

    goto/16 :goto_0

    .line 354
    :cond_b
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_off:Landroid/widget/Button;

    if-ne p1, v0, :cond_c

    .line 355
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->dialogDisplayer:Lmarto/tools/gui/menus/DialogFragmentDisplayer;

    const/4 v1, 0x1

    const v2, 0x7f0700a0

    invoke-virtual {p0, v2}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v2

    iget-wide v4, p0, Lmarto/androsdr2/SDRTouchMain;->mOffset:J

    const/4 v3, 0x1

    invoke-static {v1, v2, v4, v5, v3}, Lmarto/tools/gui/dialogs/DialogFreqChooser;->create(ILjava/lang/String;JZ)Landroid/support/v4/app/DialogFragment;

    move-result-object v1

    invoke-virtual {v0, v1}, Lmarto/tools/gui/menus/DialogFragmentDisplayer;->dialog_showOneOnlyCustom(Landroid/support/v4/app/DialogFragment;)V

    goto/16 :goto_0

    .line 356
    :cond_c
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_rec:Landroid/widget/ToggleButton;

    if-ne p1, v0, :cond_d

    .line 357
    invoke-direct {p0}, Lmarto/androsdr2/SDRTouchMain;->onRecordButtonClicked()V

    goto/16 :goto_0

    .line 358
    :cond_d
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_open:Landroid/widget/Button;

    if-ne p1, v0, :cond_e

    .line 359
    const/4 v0, 0x4

    const v1, 0x7f07009f

    invoke-virtual {p0, v1}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v1

    const/4 v2, 0x2

    new-array v2, v2, [Ljava/lang/String;

    const/4 v3, 0x0

    const v4, 0x7f07009c

    invoke-virtual {p0, v4}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v4

    aput-object v4, v2, v3

    const/4 v3, 0x1

    const v4, 0x7f07009d

    invoke-virtual {p0, v4}, Lmarto/androsdr2/SDRTouchMain;->getString(I)Ljava/lang/String;

    move-result-object v4

    aput-object v4, v2, v3

    invoke-virtual {p0, v0, v1, v2}, Lmarto/androsdr2/SDRTouchMain;->dialog_showItemsChooser(ILjava/lang/String;[Ljava/lang/String;)V

    goto/16 :goto_0

    .line 360
    :cond_e
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_gains:Landroid/widget/Button;

    if-ne p1, v0, :cond_f

    .line 361
    iget-object v8, p0, Lmarto/androsdr2/SDRTouchMain;->dialogDisplayer:Lmarto/tools/gui/menus/DialogFragmentDisplayer;

    iget v0, p0, Lmarto/androsdr2/SDRTouchMain;->mGain:I

    iget-boolean v1, p0, Lmarto/androsdr2/SDRTouchMain;->mGainSupported:Z

    iget v2, p0, Lmarto/androsdr2/SDRTouchMain;->mPpm:I

    iget-boolean v3, p0, Lmarto/androsdr2/SDRTouchMain;->mPpmSupported:Z

    iget-boolean v4, p0, Lmarto/androsdr2/SDRTouchMain;->mGainManual:Z

    iget-boolean v5, p0, Lmarto/androsdr2/SDRTouchMain;->mAutoGainSupported:Z

    iget v6, p0, Lmarto/androsdr2/SDRTouchMain;->mAudioGain:I

    invoke-static/range {v0 .. v6}, Lmarto/tools/gui/dialogs/DialogSettings;->create(IZIZZZI)Landroid/support/v4/app/DialogFragment;

    move-result-object v0

    invoke-virtual {v8, v0}, Lmarto/tools/gui/menus/DialogFragmentDisplayer;->dialog_showOneOnlyCustom(Landroid/support/v4/app/DialogFragment;)V

    goto/16 :goto_0

    .line 362
    :cond_f
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_prefs:Landroid/widget/Button;

    if-ne p1, v0, :cond_10

    .line 363
    new-instance v0, Landroid/content/Intent;

    const-class v1, Lmarto/androsdr2/SDRPreferences;

    invoke-direct {v0, p0, v1}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->startActivity(Landroid/content/Intent;)V

    goto/16 :goto_0

    .line 365
    :cond_10
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_help:Landroid/widget/Button;

    if-ne p1, v0, :cond_11

    .line 366
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->dialogDisplayer:Lmarto/tools/gui/menus/DialogFragmentDisplayer;

    invoke-static {}, Lmarto/tools/gui/dialogs/DialogHelp;->create()Landroid/support/v4/app/DialogFragment;

    move-result-object v1

    invoke-virtual {v0, v1}, Lmarto/tools/gui/menus/DialogFragmentDisplayer;->dialog_showOneOnlyCustom(Landroid/support/v4/app/DialogFragment;)V

    goto/16 :goto_0

    .line 367
    :cond_11
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_advancedrds:Landroid/widget/Button;

    if-ne p1, v0, :cond_0

    .line 368
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->dialogDisplayer:Lmarto/tools/gui/menus/DialogFragmentDisplayer;

    iget-boolean v1, p0, Lmarto/androsdr2/SDRTouchMain;->isPro:Z

    invoke-static {p0, v1}, Lmarto/tools/gui/dialogs/DialogRds;->create(Landroid/content/Context;Z)Landroid/support/v4/app/DialogFragment;

    move-result-object v1

    invoke-virtual {v0, v1}, Lmarto/tools/gui/menus/DialogFragmentDisplayer;->dialog_showOneOnlyCustom(Landroid/support/v4/app/DialogFragment;)V
    :try_end_1
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_1} :catch_0

    goto/16 :goto_0
.end method

.method protected onCommReady()V
    .locals 1

    .prologue
    .line 276
    iget-boolean v0, p0, Lmarto/androsdr2/SDRTouchMain;->shouldAutoStart:Z

    if-eqz v0, :cond_0

    .line 277
    const/4 v0, 0x0

    iput-boolean v0, p0, Lmarto/androsdr2/SDRTouchMain;->shouldAutoStart:Z

    .line 278
    iget-boolean v0, p0, Lmarto/androsdr2/SDRTouchMain;->on:Z

    if-nez v0, :cond_0

    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_onoff:Landroid/widget/Button;

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->onClick(Landroid/view/View;)V

    .line 280
    :cond_0
    return-void
.end method

.method protected onCreate(Landroid/os/Bundle;)V
    .locals 4
    .param p1, "savedInstanceState"    # Landroid/os/Bundle;
    .annotation build Landroid/annotation/SuppressLint;
        value = {
            "InflateParams"
        }
    .end annotation

    .prologue
    const/4 v3, 0x1

    .line 206
    invoke-super {p0, p1}, Lmarto/sdr/javasdr/SDRRadioActivity;->onCreate(Landroid/os/Bundle;)V

    .line 207
    invoke-direct {p0}, Lmarto/androsdr2/SDRTouchMain;->init()V

    .line 209
    invoke-virtual {p0, v3}, Lmarto/androsdr2/SDRTouchMain;->requestWindowFeature(I)Z

    .line 211
    new-instance v0, Lmarto/androsdr2/presets/PresetDBManager;

    invoke-virtual {p0}, Lmarto/androsdr2/SDRTouchMain;->getApplicationContext()Landroid/content/Context;

    move-result-object v1

    invoke-direct {v0, v1}, Lmarto/androsdr2/presets/PresetDBManager;-><init>(Landroid/content/Context;)V

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->preset_manager:Lmarto/androsdr2/presets/PresetDBManager;

    .line 213
    const v0, 0x7f03001b

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->setContentView(I)V

    .line 215
    const v0, 0x7f0d0058

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_onoff:Landroid/widget/Button;

    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_onoff:Landroid/widget/Button;

    invoke-virtual {v0, p0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 216
    const v0, 0x7f0d0068

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_show_favs:Landroid/widget/Button;

    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_show_favs:Landroid/widget/Button;

    invoke-virtual {v0, p0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 217
    const v0, 0x7f0d0065

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_show_menu:Landroid/widget/Button;

    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_show_menu:Landroid/widget/Button;

    invoke-virtual {v0, p0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 218
    const v0, 0x7f0d006c

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_hide_favs:Landroid/widget/Button;

    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_hide_favs:Landroid/widget/Button;

    invoke-virtual {v0, p0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 219
    const v0, 0x7f0d0064

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_hide_menu:Landroid/widget/Button;

    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_hide_menu:Landroid/widget/Button;

    invoke-virtual {v0, p0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 220
    const v0, 0x7f0d0060

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_open:Landroid/widget/Button;

    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_open:Landroid/widget/Button;

    invoke-virtual {v0, p0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 222
    const v0, 0x7f0d0059

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_modulation:Landroid/widget/Button;

    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_modulation:Landroid/widget/Button;

    invoke-virtual {v0, p0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 223
    const v0, 0x7f0d005a

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_advancedrds:Landroid/widget/Button;

    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_advancedrds:Landroid/widget/Button;

    invoke-virtual {v0, p0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 224
    const v0, 0x7f0d005c

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_jump:Landroid/widget/Button;

    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_jump:Landroid/widget/Button;

    invoke-virtual {v0, p0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 225
    const v0, 0x7f0d005d

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/ToggleButton;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_scan:Landroid/widget/ToggleButton;

    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_scan:Landroid/widget/ToggleButton;

    invoke-virtual {v0, p0}, Landroid/widget/ToggleButton;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 226
    const v0, 0x7f0d005e

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_off:Landroid/widget/Button;

    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_off:Landroid/widget/Button;

    invoke-virtual {v0, p0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 227
    const v0, 0x7f0d005f

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/ToggleButton;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_rec:Landroid/widget/ToggleButton;

    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_rec:Landroid/widget/ToggleButton;

    invoke-virtual {v0, p0}, Landroid/widget/ToggleButton;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 228
    const v0, 0x7f0d0061

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_gains:Landroid/widget/Button;

    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_gains:Landroid/widget/Button;

    invoke-virtual {v0, p0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 229
    const v0, 0x7f0d0062

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_prefs:Landroid/widget/Button;

    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_prefs:Landroid/widget/Button;

    invoke-virtual {v0, p0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 230
    const v0, 0x7f0d0063

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_help:Landroid/widget/Button;

    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_help:Landroid/widget/Button;

    invoke-virtual {v0, p0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 232
    const v0, 0x7f0d005b

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_fft:Landroid/widget/Button;

    .line 234
    const v0, 0x7f0d006a

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_cat:Landroid/widget/Button;

    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_cat:Landroid/widget/Button;

    invoke-virtual {v0, p0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 236
    invoke-virtual {p0}, Lmarto/androsdr2/SDRTouchMain;->getLayoutInflater()Landroid/view/LayoutInflater;

    move-result-object v0

    const v1, 0x7f03001d

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2}, Landroid/view/LayoutInflater;->inflate(ILandroid/view/ViewGroup;)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_add:Landroid/widget/Button;

    .line 237
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_add:Landroid/widget/Button;

    const-string v1, "+"

    invoke-virtual {v0, v1}, Landroid/widget/Button;->setText(Ljava/lang/CharSequence;)V

    .line 238
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_add:Landroid/widget/Button;

    invoke-virtual {v0, p0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 240
    const v0, 0x7f0d0069

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/LinearLayout;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->linlay_favs:Landroid/widget/LinearLayout;

    .line 241
    const v0, 0x7f0d0056

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/LinearLayout;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->linlay_menu:Landroid/widget/LinearLayout;

    .line 242
    const v0, 0x7f0d006b

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/LinearLayout;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->linlay_presetsplace:Landroid/widget/LinearLayout;

    .line 244
    const v0, 0x7f0d0067

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Lmarto/tools/gui/SDRAreaDisplay_Android;

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->sdrarea:Lmarto/tools/gui/SDRAreaDisplay_Android;

    .line 246
    new-instance v0, Lmarto/androsdr2/presets/PresetScanner;

    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->scanner_callback:Lmarto/androsdr2/presets/PresetScanner$ScannerCallback;

    invoke-direct {v0, v1, p0}, Lmarto/androsdr2/presets/PresetScanner;-><init>(Lmarto/androsdr2/presets/PresetScanner$ScannerCallback;Landroid/content/Context;)V

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->scanner:Lmarto/androsdr2/presets/PresetScanner;

    .line 247
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->btn_scan:Landroid/widget/ToggleButton;

    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->scanner:Lmarto/androsdr2/presets/PresetScanner;

    invoke-virtual {v1}, Lmarto/androsdr2/presets/PresetScanner;->isScanning()Z

    move-result v1

    invoke-virtual {v0, v1}, Landroid/widget/ToggleButton;->setChecked(Z)V

    .line 249
    invoke-direct {p0}, Lmarto/androsdr2/SDRTouchMain;->loadPrefs()V

    .line 251
    iget-boolean v0, p0, Lmarto/androsdr2/SDRTouchMain;->firstrun:Z

    if-eqz v0, :cond_0

    .line 252
    const/4 v0, 0x0

    iput-boolean v0, p0, Lmarto/androsdr2/SDRTouchMain;->firstrun:Z

    .line 253
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->dialogDisplayer:Lmarto/tools/gui/menus/DialogFragmentDisplayer;

    invoke-static {}, Lmarto/tools/gui/dialogs/DialogHelp;->create()Landroid/support/v4/app/DialogFragment;

    move-result-object v1

    invoke-virtual {v0, v1}, Lmarto/tools/gui/menus/DialogFragmentDisplayer;->dialog_showOneOnlyCustom(Landroid/support/v4/app/DialogFragment;)V

    .line 256
    :cond_0
    sget-object v0, Lmarto/tools/SharedConstants;->APP_LINKS:Lmarto/tools/FileSyncer;

    invoke-virtual {p0}, Lmarto/androsdr2/SDRTouchMain;->getApplicationContext()Landroid/content/Context;

    move-result-object v1

    new-instance v2, Lmarto/androsdr2/SDRTouchMain$2;

    invoke-direct {v2, p0}, Lmarto/androsdr2/SDRTouchMain$2;-><init>(Lmarto/androsdr2/SDRTouchMain;)V

    invoke-virtual {v0, v1, v2}, Lmarto/tools/FileSyncer;->sync(Landroid/content/Context;Ljava/lang/Runnable;)V

    .line 268
    const-string v0, "com.sdrtouch.rtlsdr.SDR_DEVICE_ATTACHED"

    invoke-virtual {p0}, Lmarto/androsdr2/SDRTouchMain;->getIntent()Landroid/content/Intent;

    move-result-object v1

    invoke-virtual {v1}, Landroid/content/Intent;->getAction()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_1

    .line 269
    iput-boolean v3, p0, Lmarto/androsdr2/SDRTouchMain;->shouldAutoStart:Z

    .line 270
    invoke-virtual {p0}, Lmarto/androsdr2/SDRTouchMain;->getIntent()Landroid/content/Intent;

    move-result-object v0

    const-string v1, "android.intent.action.MAIN"

    invoke-virtual {v0, v1}, Landroid/content/Intent;->setAction(Ljava/lang/String;)Landroid/content/Intent;

    .line 272
    :cond_1
    return-void
.end method

.method public onItemDialogChosen(II)V
    .locals 6
    .param p1, "dialog_id"    # I
    .param p2, "id"    # I

    .prologue
    const-wide/16 v2, 0x1

    .line 634
    packed-switch p1, :pswitch_data_0

    .line 655
    :cond_0
    :goto_0
    return-void

    .line 636
    :pswitch_0
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->SUPPORTED_MODULATIONS_AND_NAMES:Ljava/util/List;

    invoke-interface {v0, p2}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Landroid/util/Pair;

    iget-object v0, v0, Landroid/util/Pair;->first:Ljava/lang/Object;

    check-cast v0, Ljava/lang/Runnable;

    invoke-interface {v0}, Ljava/lang/Runnable;->run()V

    goto :goto_0

    .line 639
    :pswitch_1
    invoke-direct {p0, p2}, Lmarto/androsdr2/SDRTouchMain;->btn_catClicked_result(I)V

    goto :goto_0

    .line 642
    :pswitch_2
    invoke-direct {p0, p2}, Lmarto/androsdr2/SDRTouchMain;->preset_menu_clicked(I)V

    goto :goto_0

    .line 645
    :pswitch_3
    invoke-direct {p0, p2}, Lmarto/androsdr2/SDRTouchMain;->open_dialog_clicked(I)V

    goto :goto_0

    .line 648
    :pswitch_4
    if-nez p2, :cond_1

    sget-object v1, Lmarto/sdr/javasdr/SDRMessageFromClient;->SET_RECORDING_STATE:Lmarto/sdr/javasdr/SDRMessageFromClient;

    move-object v0, p0

    move-wide v4, v2

    invoke-virtual/range {v0 .. v5}, Lmarto/androsdr2/SDRTouchMain;->sdrSendMessageToServer(Lmarto/sdr/javasdr/SDRMessageFromClient;JJ)V

    .line 649
    :cond_1
    const/4 v0, 0x1

    if-ne p2, v0, :cond_0

    .line 650
    sget-object v1, Lmarto/sdr/javasdr/SDRMessageFromClient;->SET_RECORDING_STATE:Lmarto/sdr/javasdr/SDRMessageFromClient;

    const-wide/16 v4, 0x2

    move-object v0, p0

    invoke-virtual/range {v0 .. v5}, Lmarto/androsdr2/SDRTouchMain;->sdrSendMessageToServer(Lmarto/sdr/javasdr/SDRMessageFromClient;JJ)V

    goto :goto_0

    .line 634
    nop

    :pswitch_data_0
    .packed-switch 0x1
        :pswitch_0
        :pswitch_1
        :pswitch_2
        :pswitch_3
        :pswitch_4
    .end packed-switch
.end method

.method protected onPause()V
    .locals 0

    .prologue
    .line 974
    invoke-super {p0}, Lmarto/sdr/javasdr/SDRRadioActivity;->onPause()V

    .line 975
    invoke-direct {p0}, Lmarto/androsdr2/SDRTouchMain;->storePrefs()V

    .line 976
    return-void
.end method

.method protected onReceiveFromServer(Lmarto/sdr/javasdr/SDRMessageFromServer;JJLjava/lang/Object;)V
    .locals 6
    .param p1, "msg"    # Lmarto/sdr/javasdr/SDRMessageFromServer;
    .param p2, "val1"    # J
    .param p4, "val2"    # J
    .param p6, "obj"    # Ljava/lang/Object;

    .prologue
    .line 515
    sget-object v2, Lmarto/androsdr2/SDRTouchMain$14;->$SwitchMap$marto$sdr$javasdr$SDRMessageFromServer:[I

    invoke-virtual {p1}, Lmarto/sdr/javasdr/SDRMessageFromServer;->ordinal()I

    move-result v3

    aget v2, v2, v3

    packed-switch v2, :pswitch_data_0

    .line 627
    new-instance v2, Ljava/lang/Exception;

    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    const-string v4, "Unexpected message "

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-direct {v2, v3}, Ljava/lang/Exception;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0, v2}, Lmarto/androsdr2/SDRTouchMain;->onException(Ljava/lang/Exception;)V

    .line 630
    .end local p6    # "obj":Ljava/lang/Object;
    :cond_0
    :goto_0
    return-void

    .line 517
    .restart local p6    # "obj":Ljava/lang/Object;
    :pswitch_0
    const-wide/16 v2, 0x1

    cmp-long v2, p2, v2

    if-nez v2, :cond_1

    const/4 v2, 0x1

    :goto_1
    iput-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->on:Z

    .line 518
    invoke-virtual {p0}, Lmarto/androsdr2/SDRTouchMain;->checkForPro()V

    goto :goto_0

    .line 517
    :cond_1
    const/4 v2, 0x0

    goto :goto_1

    .line 521
    :pswitch_1
    const/4 v2, 0x0

    iput-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->on:Z

    .line 522
    invoke-virtual {p0}, Lmarto/androsdr2/SDRTouchMain;->saveSettings()V

    goto :goto_0

    .line 525
    :pswitch_2
    check-cast p6, Ljava/lang/Exception;

    .end local p6    # "obj":Ljava/lang/Object;
    invoke-virtual {p0, p6}, Lmarto/androsdr2/SDRTouchMain;->onException(Ljava/lang/Exception;)V

    goto :goto_0

    .line 528
    .restart local p6    # "obj":Ljava/lang/Object;
    :pswitch_3
    iget-object v2, p0, Lmarto/androsdr2/SDRTouchMain;->btn_modulation:Landroid/widget/Button;

    if-eqz v2, :cond_2

    .line 529
    new-instance v2, Lmarto/androsdr2/SDRTouchMain$4;

    invoke-direct {v2, p0, p6}, Lmarto/androsdr2/SDRTouchMain$4;-><init>(Lmarto/androsdr2/SDRTouchMain;Ljava/lang/Object;)V

    invoke-virtual {p0, v2}, Lmarto/androsdr2/SDRTouchMain;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 540
    :cond_2
    check-cast p6, Lmarto/sdr/javasdr/SDRRadio$MODULATION;

    .end local p6    # "obj":Ljava/lang/Object;
    iput-object p6, p0, Lmarto/androsdr2/SDRTouchMain;->mMod:Lmarto/sdr/javasdr/SDRRadio$MODULATION;

    goto :goto_0

    .line 543
    .restart local p6    # "obj":Ljava/lang/Object;
    :pswitch_4
    iput-wide p2, p0, Lmarto/androsdr2/SDRTouchMain;->mCentFreq:J

    .line 544
    const/4 v2, 0x0

    iput-object v2, p0, Lmarto/androsdr2/SDRTouchMain;->rdsPS:Ljava/lang/String;

    .line 545
    invoke-direct {p0}, Lmarto/androsdr2/SDRTouchMain;->recalcActivePresetButton()V

    goto :goto_0

    .line 548
    :pswitch_5
    iput-wide p2, p0, Lmarto/androsdr2/SDRTouchMain;->mVFOFreq:J

    .line 549
    const/4 v2, 0x0

    iput-object v2, p0, Lmarto/androsdr2/SDRTouchMain;->rdsPS:Ljava/lang/String;

    .line 550
    invoke-direct {p0}, Lmarto/androsdr2/SDRTouchMain;->recalcActivePresetButton()V

    goto :goto_0

    .line 553
    :pswitch_6
    iput-wide p2, p0, Lmarto/androsdr2/SDRTouchMain;->mLPwidth:J

    goto :goto_0

    .line 556
    :pswitch_7
    iput-wide p2, p0, Lmarto/androsdr2/SDRTouchMain;->mOffset:J

    goto :goto_0

    .line 559
    :pswitch_8
    const-wide/16 v2, 0x1

    cmp-long v2, p2, v2

    if-nez v2, :cond_3

    const/4 v2, 0x1

    :goto_2
    iput-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->mGainManual:Z

    .line 560
    check-cast p6, Ljava/lang/Boolean;

    .end local p6    # "obj":Ljava/lang/Object;
    invoke-virtual {p6}, Ljava/lang/Boolean;->booleanValue()Z

    move-result v2

    iput-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->mAutoGainSupported:Z

    goto :goto_0

    .line 559
    .restart local p6    # "obj":Ljava/lang/Object;
    :cond_3
    const/4 v2, 0x0

    goto :goto_2

    .line 563
    :pswitch_9
    long-to-int v2, p2

    iput v2, p0, Lmarto/androsdr2/SDRTouchMain;->mPpm:I

    .line 564
    check-cast p6, Ljava/lang/Boolean;

    .end local p6    # "obj":Ljava/lang/Object;
    invoke-virtual {p6}, Ljava/lang/Boolean;->booleanValue()Z

    move-result v2

    iput-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->mPpmSupported:Z

    goto :goto_0

    .line 567
    .restart local p6    # "obj":Ljava/lang/Object;
    :pswitch_a
    long-to-int v2, p2

    iput v2, p0, Lmarto/androsdr2/SDRTouchMain;->mGain:I

    .line 568
    check-cast p6, Ljava/lang/Boolean;

    .end local p6    # "obj":Ljava/lang/Object;
    invoke-virtual {p6}, Ljava/lang/Boolean;->booleanValue()Z

    move-result v2

    iput-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->mGainSupported:Z

    goto :goto_0

    .line 571
    .restart local p6    # "obj":Ljava/lang/Object;
    :pswitch_b
    long-to-int v2, p2

    iput v2, p0, Lmarto/androsdr2/SDRTouchMain;->mAudioGain:I

    goto :goto_0

    .line 574
    :pswitch_c
    const-wide/16 v2, 0x1

    cmp-long v2, p2, v2

    if-nez v2, :cond_4

    const/4 v2, 0x0

    iput-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->isAudioBeingRecorded:Z

    .line 575
    :cond_4
    const-wide/16 v2, 0x2

    cmp-long v2, p2, v2

    if-nez v2, :cond_5

    const/4 v2, 0x0

    iput-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->isBasebandBeingRecorded:Z

    .line 576
    :cond_5
    new-instance v2, Lmarto/androsdr2/SDRTouchMain$5;

    invoke-direct {v2, p0, p6}, Lmarto/androsdr2/SDRTouchMain$5;-><init>(Lmarto/androsdr2/SDRTouchMain;Ljava/lang/Object;)V

    invoke-virtual {p0, v2}, Lmarto/androsdr2/SDRTouchMain;->runOnUiThread(Ljava/lang/Runnable;)V

    goto/16 :goto_0

    .line 586
    :pswitch_d
    iget-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->isAudioBeingRecorded:Z

    if-nez v2, :cond_a

    iget-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->isBasebandBeingRecorded:Z

    if-nez v2, :cond_a

    const/4 v0, 0x1

    .line 587
    .local v0, "initStopped":Z
    :goto_3
    const-wide/16 v2, 0x1

    cmp-long v2, p4, v2

    if-nez v2, :cond_6

    const-wide/16 v2, 0x1

    cmp-long v2, p2, v2

    if-nez v2, :cond_b

    const/4 v2, 0x1

    :goto_4
    iput-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->isAudioBeingRecorded:Z

    .line 588
    :cond_6
    const-wide/16 v2, 0x2

    cmp-long v2, p4, v2

    if-nez v2, :cond_7

    const-wide/16 v2, 0x1

    cmp-long v2, p2, v2

    if-nez v2, :cond_c

    const/4 v2, 0x1

    :goto_5
    iput-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->isBasebandBeingRecorded:Z

    .line 589
    :cond_7
    if-eqz v0, :cond_9

    iget-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->isAudioBeingRecorded:Z

    if-nez v2, :cond_8

    iget-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->isBasebandBeingRecorded:Z

    if-eqz v2, :cond_9

    .line 590
    :cond_8
    new-instance v2, Lmarto/androsdr2/SDRTouchMain$6;

    invoke-direct {v2, p0}, Lmarto/androsdr2/SDRTouchMain$6;-><init>(Lmarto/androsdr2/SDRTouchMain;)V

    invoke-virtual {p0, v2}, Lmarto/androsdr2/SDRTouchMain;->runOnUiThread(Ljava/lang/Runnable;)V

    .line 597
    :cond_9
    if-nez v0, :cond_0

    iget-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->isAudioBeingRecorded:Z

    if-nez v2, :cond_0

    iget-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->isBasebandBeingRecorded:Z

    if-nez v2, :cond_0

    .line 598
    new-instance v2, Lmarto/androsdr2/SDRTouchMain$7;

    invoke-direct {v2, p0}, Lmarto/androsdr2/SDRTouchMain$7;-><init>(Lmarto/androsdr2/SDRTouchMain;)V

    invoke-virtual {p0, v2}, Lmarto/androsdr2/SDRTouchMain;->runOnUiThread(Ljava/lang/Runnable;)V

    goto/16 :goto_0

    .line 586
    .end local v0    # "initStopped":Z
    :cond_a
    const/4 v0, 0x0

    goto :goto_3

    .line 587
    .restart local v0    # "initStopped":Z
    :cond_b
    const/4 v2, 0x0

    goto :goto_4

    .line 588
    :cond_c
    const/4 v2, 0x0

    goto :goto_5

    .line 608
    .end local v0    # "initStopped":Z
    :pswitch_e
    new-instance v2, Lmarto/androsdr2/SDRTouchMain$8;

    invoke-direct {v2, p0, p2, p3}, Lmarto/androsdr2/SDRTouchMain$8;-><init>(Lmarto/androsdr2/SDRTouchMain;J)V

    invoke-virtual {p0, v2}, Lmarto/androsdr2/SDRTouchMain;->runOnUiThread(Ljava/lang/Runnable;)V

    goto/16 :goto_0

    .line 616
    :pswitch_f
    const-wide/16 v2, 0x3

    cmp-long v2, p2, v2

    if-nez v2, :cond_0

    move-object v1, p6

    .line 617
    check-cast v1, Lmarto/sdr/javasdr/rds/RdsData;

    .line 618
    .local v1, "rdsData":Lmarto/sdr/javasdr/rds/RdsData;
    monitor-enter v1

    .line 619
    :try_start_0
    invoke-virtual {v1}, Lmarto/sdr/javasdr/rds/RdsData;->getPS()Ljava/lang/String;

    move-result-object v2

    iput-object v2, p0, Lmarto/androsdr2/SDRTouchMain;->rdsPS:Ljava/lang/String;

    .line 620
    monitor-exit v1

    goto/16 :goto_0

    :catchall_0
    move-exception v2

    monitor-exit v1
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    throw v2

    .line 624
    .end local v1    # "rdsData":Lmarto/sdr/javasdr/rds/RdsData;
    :pswitch_10
    const-wide/16 v2, 0x1

    cmp-long v2, p2, v2

    if-nez v2, :cond_d

    const/4 v2, 0x1

    :goto_6
    iput-boolean v2, p0, Lmarto/androsdr2/SDRTouchMain;->isPro:Z

    goto/16 :goto_0

    :cond_d
    const/4 v2, 0x0

    goto :goto_6

    .line 515
    :pswitch_data_0
    .packed-switch 0x1
        :pswitch_0
        :pswitch_1
        :pswitch_2
        :pswitch_3
        :pswitch_4
        :pswitch_5
        :pswitch_6
        :pswitch_7
        :pswitch_8
        :pswitch_9
        :pswitch_a
        :pswitch_b
        :pswitch_c
        :pswitch_d
        :pswitch_e
        :pswitch_f
        :pswitch_10
    .end packed-switch
.end method

.method protected onRestart()V
    .locals 1

    .prologue
    .line 960
    invoke-super {p0}, Lmarto/sdr/javasdr/SDRRadioActivity;->onRestart()V

    .line 961
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->sdrarea:Lmarto/tools/gui/SDRAreaDisplay_Android;

    invoke-virtual {v0}, Lmarto/tools/gui/SDRAreaDisplay_Android;->parentActivityRestarted()V

    .line 962
    return-void
.end method

.method protected onStart()V
    .locals 6

    .prologue
    .line 980
    invoke-super {p0}, Lmarto/sdr/javasdr/SDRRadioActivity;->onStart()V

    .line 981
    iget-object v3, p0, Lmarto/androsdr2/SDRTouchMain;->preset_manager:Lmarto/androsdr2/presets/PresetDBManager;

    invoke-virtual {v3}, Lmarto/androsdr2/presets/PresetDBManager;->getWritableDatabase()Landroid/database/sqlite/SQLiteDatabase;

    move-result-object v3

    iput-object v3, p0, Lmarto/androsdr2/SDRTouchMain;->preset_db:Landroid/database/sqlite/SQLiteDatabase;

    .line 983
    iget-object v3, p0, Lmarto/androsdr2/SDRTouchMain;->lastCatName:Ljava/lang/String;

    if-eqz v3, :cond_0

    .line 984
    invoke-static {}, Lmarto/androsdr2/presets/Category;->getRoot()Lmarto/androsdr2/presets/Category;

    move-result-object v2

    .line 985
    .local v2, "rootcat":Lmarto/androsdr2/presets/Category;
    iget-object v3, p0, Lmarto/androsdr2/SDRTouchMain;->lastCatName:Ljava/lang/String;

    iget-object v4, v2, Lmarto/androsdr2/presets/Category;->name:Ljava/lang/String;

    invoke-virtual {v3, v4}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v3

    if-eqz v3, :cond_1

    .line 986
    sput-object v2, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    .line 997
    .end local v2    # "rootcat":Lmarto/androsdr2/presets/Category;
    :cond_0
    :goto_0
    sget-object v3, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    invoke-direct {p0, v3}, Lmarto/androsdr2/SDRTouchMain;->createAllButtonsFor(Lmarto/androsdr2/presets/Category;)V

    .line 998
    return-void

    .line 988
    .restart local v2    # "rootcat":Lmarto/androsdr2/presets/Category;
    :cond_1
    iget-object v3, p0, Lmarto/androsdr2/SDRTouchMain;->preset_db:Landroid/database/sqlite/SQLiteDatabase;

    invoke-static {v3}, Lmarto/androsdr2/presets/PresetDBManager;->getAllCategories(Landroid/database/sqlite/SQLiteDatabase;)Ljava/util/Collection;

    move-result-object v1

    .line 989
    .local v1, "categories":Ljava/util/Collection;, "Ljava/util/Collection<Lmarto/androsdr2/presets/Category;>;"
    invoke-interface {v1}, Ljava/util/Collection;->iterator()Ljava/util/Iterator;

    move-result-object v3

    :cond_2
    invoke-interface {v3}, Ljava/util/Iterator;->hasNext()Z

    move-result v4

    if-eqz v4, :cond_0

    invoke-interface {v3}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lmarto/androsdr2/presets/Category;

    .line 990
    .local v0, "c":Lmarto/androsdr2/presets/Category;
    iget-object v4, v0, Lmarto/androsdr2/presets/Category;->name:Ljava/lang/String;

    iget-object v5, p0, Lmarto/androsdr2/SDRTouchMain;->lastCatName:Ljava/lang/String;

    invoke-virtual {v4, v5}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v4

    if-eqz v4, :cond_2

    .line 991
    sput-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    goto :goto_0
.end method

.method protected onStop()V
    .locals 1

    .prologue
    .line 966
    invoke-super {p0}, Lmarto/sdr/javasdr/SDRRadioActivity;->onStop()V

    .line 967
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->sdrarea:Lmarto/tools/gui/SDRAreaDisplay_Android;

    invoke-virtual {v0}, Lmarto/tools/gui/SDRAreaDisplay_Android;->parentActivityStopped()V

    .line 968
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->preset_db:Landroid/database/sqlite/SQLiteDatabase;

    invoke-virtual {v0}, Landroid/database/sqlite/SQLiteDatabase;->close()V

    .line 969
    const/4 v0, 0x0

    iput-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->preset_db:Landroid/database/sqlite/SQLiteDatabase;

    .line 970
    return-void
.end method

.method public onTextWritten(ILjava/lang/String;)V
    .locals 2
    .param p1, "dialog_id"    # I
    .param p2, "text"    # Ljava/lang/String;

    .prologue
    .line 1002
    packed-switch p1, :pswitch_data_0

    .line 1050
    :goto_0
    return-void

    .line 1004
    :pswitch_0
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    if-eqz v0, :cond_0

    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->latest_preset:Lmarto/androsdr2/presets/Preset;

    if-nez v0, :cond_1

    .line 1005
    :cond_0
    new-instance v0, Ljava/lang/RuntimeException;

    const-string v1, "Cannot add a new preset."

    invoke-direct {v0, v1}, Ljava/lang/RuntimeException;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->onException(Ljava/lang/Exception;)V

    goto :goto_0

    .line 1008
    :cond_1
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->latest_preset:Lmarto/androsdr2/presets/Preset;

    iput-object p2, v0, Lmarto/androsdr2/presets/Preset;->name:Ljava/lang/String;

    .line 1009
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->latest_preset:Lmarto/androsdr2/presets/Preset;

    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->preset_db:Landroid/database/sqlite/SQLiteDatabase;

    invoke-static {v0, v1}, Lmarto/androsdr2/presets/PresetDBManager;->addOrEditPreset(Lmarto/androsdr2/presets/Preset;Landroid/database/sqlite/SQLiteDatabase;)V

    .line 1010
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    invoke-direct {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->createAllButtonsFor(Lmarto/androsdr2/presets/Category;)V

    goto :goto_0

    .line 1013
    :pswitch_1
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    if-nez v0, :cond_2

    .line 1014
    new-instance v0, Ljava/lang/RuntimeException;

    const-string v1, "Cannot add a new category."

    invoke-direct {v0, v1}, Ljava/lang/RuntimeException;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->onException(Ljava/lang/Exception;)V

    goto :goto_0

    .line 1017
    :cond_2
    new-instance v0, Lmarto/androsdr2/presets/Category;

    invoke-direct {v0, p2}, Lmarto/androsdr2/presets/Category;-><init>(Ljava/lang/String;)V

    sput-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    .line 1018
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->preset_db:Landroid/database/sqlite/SQLiteDatabase;

    invoke-static {v0, v1}, Lmarto/androsdr2/presets/PresetDBManager;->addOrEditCategory(Lmarto/androsdr2/presets/Category;Landroid/database/sqlite/SQLiteDatabase;)V

    .line 1019
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    invoke-direct {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->createAllButtonsFor(Lmarto/androsdr2/presets/Category;)V

    goto :goto_0

    .line 1022
    :pswitch_2
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    if-eqz v0, :cond_3

    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currPreset:Lmarto/androsdr2/presets/Preset;

    if-nez v0, :cond_4

    .line 1023
    :cond_3
    new-instance v0, Ljava/lang/RuntimeException;

    const-string v1, "Cannot rename a preset."

    invoke-direct {v0, v1}, Ljava/lang/RuntimeException;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->onException(Ljava/lang/Exception;)V

    goto :goto_0

    .line 1026
    :cond_4
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currPreset:Lmarto/androsdr2/presets/Preset;

    iput-object p2, v0, Lmarto/androsdr2/presets/Preset;->name:Ljava/lang/String;

    .line 1027
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currPreset:Lmarto/androsdr2/presets/Preset;

    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->preset_db:Landroid/database/sqlite/SQLiteDatabase;

    invoke-static {v0, v1}, Lmarto/androsdr2/presets/PresetDBManager;->addOrEditPreset(Lmarto/androsdr2/presets/Preset;Landroid/database/sqlite/SQLiteDatabase;)V

    .line 1028
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    invoke-direct {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->createAllButtonsFor(Lmarto/androsdr2/presets/Category;)V

    goto :goto_0

    .line 1031
    :pswitch_3
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    if-nez v0, :cond_5

    .line 1032
    new-instance v0, Ljava/lang/RuntimeException;

    const-string v1, "Cannot rename a category."

    invoke-direct {v0, v1}, Ljava/lang/RuntimeException;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->onException(Ljava/lang/Exception;)V

    goto :goto_0

    .line 1035
    :cond_5
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    iput-object p2, v0, Lmarto/androsdr2/presets/Category;->name:Ljava/lang/String;

    .line 1036
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->preset_db:Landroid/database/sqlite/SQLiteDatabase;

    invoke-static {v0, v1}, Lmarto/androsdr2/presets/PresetDBManager;->addOrEditCategory(Lmarto/androsdr2/presets/Category;Landroid/database/sqlite/SQLiteDatabase;)V

    .line 1037
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    invoke-direct {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->createAllButtonsFor(Lmarto/androsdr2/presets/Category;)V

    goto/16 :goto_0

    .line 1040
    :pswitch_4
    iput-object p2, p0, Lmarto/androsdr2/SDRTouchMain;->remote:Ljava/lang/String;

    .line 1041
    const-string v0, "://"

    invoke-virtual {p2, v0}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v0

    if-eqz v0, :cond_6

    .line 1042
    invoke-static {p2}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    move-result-object v0

    invoke-direct {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->remoteStart(Landroid/net/Uri;)V

    goto/16 :goto_0

    .line 1044
    :cond_6
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "http://"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    move-result-object v0

    invoke-direct {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->remoteStart(Landroid/net/Uri;)V

    goto/16 :goto_0

    .line 1002
    nop

    :pswitch_data_0
    .packed-switch 0x1
        :pswitch_0
        :pswitch_1
        :pswitch_2
        :pswitch_3
        :pswitch_4
    .end packed-switch
.end method

.method public onYes(I)V
    .locals 3
    .param p1, "dialog_id"    # I

    .prologue
    .line 1054
    packed-switch p1, :pswitch_data_0

    .line 1084
    :goto_0
    return-void

    .line 1056
    :pswitch_0
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    if-nez v0, :cond_0

    .line 1057
    new-instance v0, Ljava/lang/RuntimeException;

    const-string v1, "Cannot delete a category."

    invoke-direct {v0, v1}, Ljava/lang/RuntimeException;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->onException(Ljava/lang/Exception;)V

    goto :goto_0

    .line 1060
    :cond_0
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->preset_db:Landroid/database/sqlite/SQLiteDatabase;

    invoke-static {v0, v1}, Lmarto/androsdr2/presets/PresetDBManager;->deleteCategory(Lmarto/androsdr2/presets/Category;Landroid/database/sqlite/SQLiteDatabase;)V

    .line 1061
    invoke-static {}, Lmarto/androsdr2/presets/Category;->getRoot()Lmarto/androsdr2/presets/Category;

    move-result-object v0

    sput-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    .line 1062
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    invoke-direct {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->createAllButtonsFor(Lmarto/androsdr2/presets/Category;)V

    goto :goto_0

    .line 1065
    :pswitch_1
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    if-eqz v0, :cond_1

    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currPreset:Lmarto/androsdr2/presets/Preset;

    if-nez v0, :cond_2

    .line 1066
    :cond_1
    new-instance v0, Ljava/lang/RuntimeException;

    const-string v1, "Cannot delete a preset."

    invoke-direct {v0, v1}, Ljava/lang/RuntimeException;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->onException(Ljava/lang/Exception;)V

    goto :goto_0

    .line 1069
    :cond_2
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currPreset:Lmarto/androsdr2/presets/Preset;

    iget-object v1, p0, Lmarto/androsdr2/SDRTouchMain;->preset_db:Landroid/database/sqlite/SQLiteDatabase;

    invoke-static {v0, v1}, Lmarto/androsdr2/presets/PresetDBManager;->deletePreset(Lmarto/androsdr2/presets/Preset;Landroid/database/sqlite/SQLiteDatabase;)V

    .line 1070
    sget-object v0, Lmarto/androsdr2/SDRTouchMain;->currCategory:Lmarto/androsdr2/presets/Category;

    invoke-direct {p0, v0}, Lmarto/androsdr2/SDRTouchMain;->createAllButtonsFor(Lmarto/androsdr2/presets/Category;)V

    goto :goto_0

    .line 1073
    :pswitch_2
    invoke-direct {p0}, Lmarto/androsdr2/SDRTouchMain;->exportPresets()V

    goto :goto_0

    .line 1076
    :pswitch_3
    invoke-direct {p0}, Lmarto/androsdr2/SDRTouchMain;->importPresets()V

    goto :goto_0

    .line 1079
    :pswitch_4
    iget-object v0, p0, Lmarto/androsdr2/SDRTouchMain;->appLinkingInfo:Lmarto/tools/linking/OtherApps;

    sget-object v1, Lmarto/tools/linking/OtherApps$App;->SDR_TOUCH:Lmarto/tools/linking/OtherApps$App;

    invoke-virtual {p0}, Lmarto/androsdr2/SDRTouchMain;->getApplicationContext()Landroid/content/Context;

    move-result-object v2

    invoke-virtual {v0, v1, v2}, Lmarto/tools/linking/OtherApps;->install(Lmarto/tools/linking/OtherApps$App;Landroid/content/Context;)V

    goto :goto_0

    .line 1054
    :pswitch_data_0
    .packed-switch 0x1
        :pswitch_0
        :pswitch_1
        :pswitch_2
        :pswitch_3
        :pswitch_4
    .end packed-switch
.end method
