# Sorry about this, I'm not a UI developer

from tkinter import *
from tkinter import ttk
from address_checks import *

class HeapSimGui:
    def __init__(self):
        # Setup title and main window
        self.root  = Tk(baseName = "Z64 Heap Simulator")
        self.root.minsize(750, 700)
        img = PhotoImage(file = 'zelda.png')
        self.root.iconphoto(False, img)
        self.root.wm_title("Z64 Heap Simulator")
        # Setup the frame we'll be using
        self.frame = ttk.Frame(self.root, padding=10, width=750, height=700)
        self.frame.grid_propagate(0)
        self.frame.grid()
        # All tracked stringVars
        self.stringVars = {}
        self.tracked    = {}
        # Setup GUI
        self.simulatorSetup()

    ## Private

    def __updateFuncList(self, *args):
        scene = self.getStringVar("scene").get()
        menu  = self.getTracked('function menu')

        classPick = None
        if scene == 'Lost Woods':
            classPick = LostWoods
        elif scene == 'Goron City':
            classPick = GoronCity

        funcList = [func for func in dir(classPick) if callable(getattr(classPick, func)) and not func.startswith("__") and "info" not in func]

        parentName = menu.winfo_parent()
        parent = menu._nametowidget(parentName)

        self.fnListSetup(parent, old=menu, funcList=funcList)

    def __triggerWriteEvent(self, sv):
        text = self.getStringVar(sv).get()
        self.getStringVar(sv).set(text)

    ## Public

    def setStringVar(self, name, sv):
        self.stringVars[name] = sv

    def getStringVar(self, name):
        return self.stringVars[name]

    def addTracked(self, name, w):
        self.tracked[name] = w

    def getTracked(self, name):
        return self.tracked[name]

    ## Simulator Setup

    def simulatorSetup(self):
        simArea = LabelFrame(self.frame, text="Simulator Setup")
        simArea.grid(column=0, row=0, padx=5, pady=5, rowspan=4)
        self.sceneSetup(simArea, callback=self.__updateFuncList)
        self.versionSetup(simArea)
        self.fnListSetup(simArea)
        self.stateFlagsSetup(simArea)
        self.addressesSetup(simArea)

        sceneArea = LabelFrame(self.frame, text="Scene Setup")
        sceneArea.grid(column=1, row=0, padx=5, pady=5)
        self.setupSetup(sceneArea)
        self.roomSetup(sceneArea)

        outputArea = LabelFrame(self.frame, text="Output")
        outputArea.grid(column=1, row=1, padx=5, pady=5, rowspan=3, sticky="nsew")
        outputArea.columnconfigure(0, minsize=425)
        self.outputSetup(outputArea)

        buttonArea = ttk.Frame(self.frame)
        buttonArea.grid(column=0, row=4, sticky="nsew")
        self.buttonsSetup(buttonArea)

    ## Individual GUI Setup Functions

    def buttonsSetup(self, parent):
        runButton  = Button(parent, text = "Run Simulation", callback = None)
        quitButton = Button(parent, text = "Quit", callback = None)

        runButton.pack(side='left', anchor='nw', padx=3, pady=3)
        quitButton.pack(side='left', anchor='nw', padx=3, pady=3)

    def outputSetup(self, parent):
        output = StringVar()
        outputArea = Message(parent, textvariable = output)
        outputArea.grid(column=0, row=0, padx=5, pady=5, sticky="w")
        outputArea.config(width=425)
        output.set("Waiting for simulator...")
        self.setStringVar("output", output)
        pass

    def setupSetup(self, parent, callback = None):
        label = Label(parent, text = 'Setup ID')
        label.pack(side='top', anchor='nw', padx=3, pady=3)
        setup = StringVar()
        setupEntry = Entry(parent, textvariable = setup)
        setupEntry.pack(side='top', anchor='nw', padx=3, pady=3)
        self.setStringVar("setup", setup)

    def roomSetup(self, parent, callback = None):
        label = Label(parent, text = 'Room ID')
        label.pack(side='top', anchor='nw', padx=3, pady=3)
        room = StringVar()
        roomEntry = Entry(parent, textvariable = room)
        roomEntry.pack(side='top', anchor='nw', padx=3, pady=3)
        self.setStringVar("room", roomEntry)

    def sceneSetup(self, parent, callback = None):
        scenes = ('Lost Woods', 'Goron City')
        scenesString = StringVar()
        self.setStringVar('scene', scenesString)
        scenesString.set(scenes[0])
        scenesString.trace_add("write", callback)

        menu = OptionMenu(parent, scenesString, *scenes)
        menu.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

        label = Label(parent, text='Scene')
        label.grid(column=0, row=0, sticky="e")

    def versionSetup(self, parent, callback = None):
        versions = (
            'OoT-N-1.0',
            'OoT-N-1.1',
            'OoT-P-1.0',
            'OoT-N-1.2',
            'OoT-P-1.1',
            'OoT-J-GC-MQDisc',
            'OoT-J-MQ',
            'OoT-U-GC',
            'OoT-U-MQ',
            'OoT-P-GC',
            'OoT-P-MQ',
            'OoT-J-GC-CEDisc',
            'OoT-iQue'
        )

        versionString = StringVar()
        self.setStringVar('version', versionString)
        versionString.set(versions[0])
        menu = OptionMenu(parent, versionString, *versions)
        menu.grid(column=1, row=1, padx=5, pady=5)
        menu.config(width=28)

        label = Label(parent, text='Version')
        label.grid(column=0, row=1, sticky="e")


    def fnListSetup(self, parent, callback = None, old = None, funcList = None):
        if old is not None:
            old.destroy()

        if funcList is None:
            funcs = ('Waiting for scene update...', '...')
        else:
            funcs = funcList
        funcsString = StringVar()
        funcsString.set(funcs[0])

        menu = OptionMenu(parent, funcsString, *funcs)
        menu.grid(column=1, row=2, padx=5, pady=5, sticky="nsew")

        label = Label(parent, text='Fn')
        label.grid(column=0, row=2, sticky="e")

        self.addTracked('function menu', menu)
        self.__triggerWriteEvent('scene')

    def stateFlagsSetup(self, parent):
        area = LabelFrame(parent, text='State Flags')
        area.grid(column=0, row=3, padx=15, pady=15, columnspan=2)

        flags = {
            'lullaby':     Checkbutton(area, text = 'lullaby'),
            'saria':       Checkbutton(area, text = 'saria'),
            'bombchu':     Checkbutton(area, text = 'bombchu'),
            'bomb':        Checkbutton(area, text = 'bomb'),
            'bottle':      Checkbutton(area, text = 'bottle'),
            'hookshot':    Checkbutton(area, text = 'hookshot'),
            'beanPlanted': Checkbutton(area, text = 'beanPlanted'),
        }
        self.addTracked("flags", flags)

        for k in flags.keys():
            flags[k].pack(side='top', anchor='w', padx=3, pady=3)

        inputArea = LabelFrame(area, text='Separate with commas')
        inputArea.pack(side='top', anchor='w', padx=10, pady=10)

        flagInputs = {
            'clearedRoomsText':     Label(inputArea, text = 'clearedRooms'),
            'clearedRooms':         Entry(inputArea),
            'switchFlagsText':      Label(inputArea, text = 'switchFlags'),
            'switchFlags':          Entry(inputArea),
            'collectibleFlagsText': Label(inputArea, text = 'collectibleFlags'),
            'collectibleFlags':     Entry(inputArea),
        }
        self.addTracked("flag inputs", flagInputs)

        for k in flagInputs.keys():
            flagInputs[k].pack(side='top', anchor='nw', padx=3, pady=3)

    def addressesSetup(self, parent, callback = None):
        label = Label(parent, text = 'Address')
        label.grid(column=0, row=4, padx=5, pady=5, sticky="w")

        address = StringVar()
        addressEntry = Entry(parent, textvariable = address)
        addressEntry.grid(column=1, row=4, padx=5, pady=5, sticky="w")

        self.setStringVar("address", address)


heapSim = HeapSimGui()
heapSim.root.mainloop()