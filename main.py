from functools import partial
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from controller import *
from masks import MaskedWidget


class Main:

    def __init__(self, master=None):
        # Master window configuration
        self.width = master.winfo_screenwidth()
        self.height = master.winfo_screenheight()
        master.geometry('%dx%d+0+0' % (self.width - 50, self.height - 90))

        self.font = ('Consolas', 13)
        self.font2 = ('Consolas', 12)
        self.fontInputs = ('Bahnschrift SemiLight', 13)
        self.fontTitle = ("Century Gothic", 18)
        self.fgTitle = 'black'
        self.bg = '#FBFCFC'
        self.bgButtonR = '#A93226'
        self.bgButtonG = '#007e33'
        self.fgButton = 'white'
        self.fontButton = ('Fixedsys', 12)

        master['bg'] = self.bg

        # Main window frame
        self.frameMain = Frame(master, bg=self.bg)
        self.frameMain.pack(side=TOP, anchor=CENTER, fill='both', expand=True)

        # Columns' head from Main window
        self.mainTreeHead = ("NOME", "CARGO", "MOTIVO DE AFASTAMENTO", 'DEPARTAMENTO', 'PRÓXIMA DATA')

        # Title main window
        self.Title = Frame(self.frameMain, bg=self.bg, padx=30, pady=5)
        self.Title.pack(fill='x', pady=25)

        self.title = Label(self.Title, text='PROJETO READAPTAR', bg=self.bg, fg=self.fgTitle, font=self.fontTitle)
        self.title.pack(anchor=W)

        # Main window's options and buttons
        self.containerOptions = Frame(self.frameMain, bg=self.bg)
        self.containerOptions.pack(fill='x', padx=30)

        self.buttonInsert = Button(self.containerOptions, text='Inserir servidor', bg=self.bgButtonG, fg=self.fgButton,
                                   font=self.fontButton, relief=GROOVE, borderwidth=2, command=self.mainToInsert)
        self.buttonInsert.pack(side=LEFT)

        self.buttonSearch = Button(self.containerOptions, text='Buscar', bg=self.bgButtonR, fg=self.fgButton,
                                   font=self.fontButton, relief=GROOVE, borderwidth=1, command=self.search)
        self.buttonSearch.pack(side=RIGHT, padx=10)

        self.etSearch = ttk.Entry(self.containerOptions, font=self.fontInputs, width=30)
        self.etSearch.pack(side=RIGHT)

        self.frameCheckBts = Frame(self.containerOptions, bg=self.bg, )
        self.frameCheckBts.pack(side=RIGHT, padx=30)

        self.varClassific = None

        self.varClassificAll = IntVar()
        self.buttonAll = Checkbutton(self.frameCheckBts, bg=self.bg, font=self.font, variable=self.varClassificAll,
                                     text='TODOS', )
        self.buttonAll['command'] = partial(self.checkClassification, self.buttonAll)
        self.buttonAll.pack(side=RIGHT)

        self.varClassificHu = IntVar()
        self.buttonHu = Checkbutton(self.frameCheckBts, bg=self.bg, font=self.font, variable=self.varClassificHu,
                                    text='HU')
        self.buttonHu['command'] = partial(self.checkClassification, self.buttonHu)
        self.buttonHu.pack(side=RIGHT)

        self.varClassificUfma = IntVar()
        self.buttonUfma = Checkbutton(self.frameCheckBts, bg=self.bg, font=self.font, variable=self.varClassificUfma,
                                      text='UFMA')
        self.buttonUfma['command'] = partial(self.checkClassification, self.buttonUfma)
        self.buttonUfma.pack(side=RIGHT)

        # Servers' table
        self.containerMain = Frame(self.frameMain, bg='green', relief=GROOVE)
        self.containerMain.pack(fill='both', padx=30, pady=5)

        self.treeServers = ttk.Treeview(columns=self.mainTreeHead, height=23, selectmode='extended', show="headings")
        self.vsb = ttk.Scrollbar(orient="vertical", command=self.treeServers.yview)
        self.treeServers.configure(yscrollcommand=self.vsb.set)
        self.treeServers.pack(side=LEFT, fill='both', expand=True, in_=self.containerMain)
        self.vsb.pack(side=RIGHT, fill='y', in_=self.containerMain)
        self.treeServers.bind("<<TreeviewSelect>>", self.on_mainTree_select1)
        self.treeServers.bind("<Double-Button-1>", self.on_mainTree_select2)

        self.containerMain.grid_columnconfigure(0, weight=1)
        self.containerMain.grid_rowconfigure(0, weight=1)

        for col in self.mainTreeHead:
            self.treeServers.heading(col, text=col.title(), command=lambda c=col: self.sortby(self.treeServers, c, 0))
        self.treeServers.column(0, width=110)
        self.treeServers.column(1, width=110)
        self.treeServers.column(2, width=110)
        self.treeServers.column(3, width=110)
        self.treeServers.column(4, width=10)

        # Verify if there was a Insert
        # self.verify=True

        # Load de servers' table
        self.loadServersTree(self.varClassific)

        # Options server
        self.optionServerFrame = Frame(self.frameMain)
        self.optionServerFrame.pack()

        self.serverSelected = None

        self.btExcludeProfile = Button(self.optionServerFrame, text='Excluir', bg=self.bgButtonR, fg=self.fgButton,
                                       font=self.fontButton, relief=GROOVE, borderwidth=1, command=self.excludeServer)
        self.btExcludeProfile.pack(side=LEFT, padx=3)

        # Insert window frame
        self.frameInsert = Frame(master, bg=self.bg)

        # Title insert window
        self.frameTitle = Frame(self.frameInsert, bg=self.bg, padx=20, pady=10)
        self.frameTitle.grid(column=1, columnspan=4, pady=25)

        self.lbTitle = Label(self.frameTitle, text='INSERIR SERVIDOR', font=self.fontTitle, bg=self.bg, fg=self.fgTitle)
        self.lbTitle.grid()

        # Servers
        self.frameServ = Frame(self.frameInsert, bg=self.bg, relief=GROOVE, borderwidth=2)
        self.frameServ.grid(row=1, column=1, rowspan=2, sticky=NW, padx=5)

        # Name
        self.frameName = Frame(self.frameServ, bg=self.bg, padx=10, pady=10)
        self.frameName.grid()

        self.lbName = Label(self.frameName, bg=self.bg, font=self.font, text='Nome:')
        self.lbName.grid(sticky=W)

        self.etName = Entry(self.frameName, width=50, font=self.fontInputs)
        self.etName.grid()

        # Office
        self.frameOffice = Frame(self.frameServ, bg=self.bg, padx=10, pady=10)
        self.frameOffice.grid()

        self.lbOffice = Label(self.frameOffice, bg=self.bg, font=self.font, text='Cargo:')
        self.lbOffice['font'] = self.font
        self.lbOffice.grid(sticky=W)

        self.etOffice = Entry(self.frameOffice, font=self.fontInputs, width=50)
        self.etOffice.grid()

        # Current Sector
        self.frameDepartament = Frame(self.frameServ, bg=self.bg, padx=10, pady=10)
        self.frameDepartament.grid()

        self.lbDepartament = Label(self.frameDepartament, bg=self.bg, font=self.font, text='Setor atual:')
        self.lbDepartament.grid(sticky=W)

        self.etDepartament = Entry(self.frameDepartament, width=50, font=self.fontInputs)
        self.etDepartament.grid()

        # Reason
        self.frameReason = Frame(self.frameServ, bg=self.bg, padx=10, pady=10)
        self.frameReason.grid()

        self.lbReason = Label(self.frameReason, bg=self.bg, font=self.font, text='Motivo do afastamento:')
        self.lbReason.grid(row=0, sticky=W)

        self.etReason = Entry(self.frameReason, width=50, font=self.fontInputs)
        self.etReason.grid(row=1)

        # Contact
        self.frameContact = Frame(self.frameReason, bg=self.bg, pady=5)
        self.frameContact.grid(row=2, sticky=W)

        self.lbContact = Label(self.frameContact, bg=self.bg, font=self.font, text='Contato:')
        self.lbContact.grid(sticky=W)

        # Type
        self.frameType = Frame(self.frameReason, bg=self.bg, pady=10)
        self.frameType.grid(row=2, sticky=E)

        self.lbtype = Label(self.frameType, bg=self.bg, font=self.font, text='Tipo:')
        self.lbtype.grid(row=1, column=2, sticky=W)

        self.Type = None

        self.varHu = IntVar()
        self.btHu = Checkbutton(self.frameType, text='HU', bg=self.bg, font=self.font2, variable=self.varHu)
        self.btHu['command'] = partial(self.checkType, self.btHu)
        self.btHu.grid(row=2, column=3)

        self.varUfma = IntVar()
        self.btUfma = Checkbutton(self.frameType, text='UFMA', bg=self.bg, font=self.font2, variable=self.varUfma)
        self.btUfma['command'] = partial(self.checkType, self.btUfma)
        self.btUfma.grid(row=2, column=2)

        # Process container
        self.frameNumProcess = Frame(self.frameServ, bg=self.bg, padx=10)
        self.frameNumProcess.grid(pady=5)

        self.lbNprocess = Label(self.frameNumProcess, text='Número do processo:', bg=self.bg, font=self.font, pady=10)
        self.lbNprocess.grid(sticky=W)

        self.frameNprocess = Frame(self.frameServ, bg=self.bg, padx=10)
        self.frameNprocess.grid(sticky=NW, pady=5)

        # Process type
        self.lbType_process = Label(self.frameNprocess, text='Tipo do processo:', bg=self.bg, font=self.font)
        self.lbType_process.grid(sticky=W)

        self.type_pro = None

        self.varAcl = IntVar()
        self.checkLca = Checkbutton(self.frameNprocess, text='Avaliação da Capacidade Laboral', bg=self.bg,
                                    font=self.font2, variable=self.varAcl)
        self.checkLca.grid(sticky=W)
        self.checkLca['command'] = partial(self.checkTypePro, self.checkLca)

        self.varRa = IntVar()
        self.checkRa = Checkbutton(self.frameNprocess, text='Restrição de atividades', bg=self.bg, font=self.font2,
                                   variable=self.varRa)
        self.checkRa.grid(sticky=W)
        self.checkRa['command'] = partial(self.checkTypePro, self.checkRa)

        self.varR = IntVar()
        self.checkR = Checkbutton(self.frameNprocess, text='Readaptação', bg=self.bg, font=self.font2,
                                  variable=self.varR)
        self.checkR.grid(sticky=W)
        self.checkR['command'] = partial(self.checkTypePro, self.checkR)

        # Dates
        self.frameDatesAndButtons = Frame(self.frameInsert, bg=self.bg, relief=GROOVE, borderwidth=0)
        self.frameDatesAndButtons.grid(row=1, column=2, sticky=NW, padx=5)

        self.frameDate = Frame(self.frameDatesAndButtons, bg=self.bg, relief=GROOVE, borderwidth=2)
        self.frameDate.grid(sticky=N)

        # Biannually
        self.frameBi = Frame(self.frameDate, bg=self.bg, padx=50, pady=10)
        self.frameBi.pack(fill='x')

        self.lbBi = Label(self.frameBi, bg=self.bg, font=self.font, text='Avaliação da perícia:')
        self.lbBi.grid()

        self.lbLd_Bi = Label(self.frameBi, bg=self.bg, font=self.font, text='Última avaliação:')
        self.lbLd_Bi.grid(row=1, sticky=W)

        self.lbNd_Bi = Label(self.frameBi, bg=self.bg, font=self.font, text='Próxima avaliação:')
        self.lbNd_Bi.grid(row=3, sticky=W)

        # Quarterly
        self.frameQua = Frame(self.frameDate, bg=self.bg, padx=50, pady=10)
        self.frameQua.pack(fill='x')

        self.lbQua = Label(self.frameQua, bg=self.bg, font=self.font, text='Avaliação do Readaptar:')
        self.lbQua.grid()

        self.lbLd_Qua = Label(self.frameQua, bg=self.bg, font=self.font, text='Última avaliação:')
        self.lbLd_Qua.grid(row=1, sticky=W)

        self.lbNd_Qua = Label(self.frameQua, bg=self.bg, font=self.font, text='Próxima avaliação:')
        self.lbNd_Qua.grid(row=3, sticky=W)

        # Buttons Save e Back
        self.frameButtons = Frame(self.frameInsert, bg=self.bg, relief=GROOVE, borderwidth=0)
        self.frameButtons.grid(row=1, column=3, padx=90)

        self.Save = Button(self.frameButtons, text='Salvar', bg=self.bgButtonG, font=self.fontButton, fg=self.fgButton,
                           width=15, command=self.insertServers)
        self.Save.grid(column=1, pady=5, padx=10)

        self.Cancel = Button(self.frameButtons, text='Voltar', bg=self.bgButtonR, font=self.fontButton,
                             fg=self.fgButton, width=15, command=self.insertToMain)
        self.Cancel.grid(row=1, column=1, pady=5, padx=10)

        # Remarks
        self.frameRemark = Frame(self.frameInsert, bg=self.bg, relief=GROOVE, borderwidth=2)
        self.frameRemark.grid(row=2, columnspan=2, sticky=W, column=2, padx=5)

        self.treeRemarkHead = ("Observações", 'data')
        self.remarks = []

        self.frameTreeRemark = Frame(self.frameRemark, bg=self.bg)
        self.frameTreeRemark.grid(padx=5, pady=5)

        self.treeRemark = ttk.Treeview(columns=self.treeRemarkHead, show="headings", height=11)
        self.sbRemark = ttk.Scrollbar(orient="vertical", command=self.treeRemark.yview)
        self.treeRemark.configure(yscrollcommand=self.sbRemark.set)
        self.treeRemark.grid(in_=self.frameTreeRemark)
        self.sbRemark.grid(column=1, row=0, sticky='ns', in_=self.frameTreeRemark)
        self.treeRemark.bind("<<TreeviewSelect>>", self.on_mainTreeRemark_select1)
        self.treeRemark.bind("<Double-Button-1>", self.on_mainTreeRemark_select2)

        for col in self.treeRemarkHead:
            self.treeRemark.heading(col, text=col.title())
        self.treeRemark.column(0, width=180)
        self.treeRemark.column(1, width=110)

        self.frameOpRemark = Frame(self.frameRemark, bg=self.bg)
        self.frameOpRemark.grid(row=0, column=3, padx=50)

        self.insertRemark = Button(self.frameOpRemark, text='Inserir observação', bg=self.bgButtonG,
                                   font=self.fontButton, fg=self.fgButton, width=25, command=self.newRemark)
        self.insertRemark.grid(pady=5)

        # Profile window frame
        self.Profile = Frame(master, bg=self.bg)

        self.server = None

        # Title insert window
        self.frameTitleProfile = Frame(self.Profile, bg=self.bg, padx=20, pady=10)
        self.frameTitleProfile.grid(column=1, columnspan=4, pady=25)

        self.lbTitleProfile = Label(self.frameTitleProfile, text='PERFIL PESSOAL', font=self.fontTitle, fg=self.fgTitle,
                                    bg=self.bg)
        self.lbTitleProfile.grid()

        # Servers
        self.frameServProfile = Frame(self.Profile, bg=self.bg, relief=GROOVE, borderwidth=2)
        self.frameServProfile.grid(row=1, column=1, rowspan=2, sticky=NW, padx=5)

        # Name
        self.frameNameProfile = Frame(self.frameServProfile, bg=self.bg, padx=10, pady=10)
        self.frameNameProfile.grid()

        self.lbNameProfile = Label(self.frameNameProfile, bg=self.bg, font=self.font, text='Nome:')
        self.lbNameProfile.grid(sticky=W)

        self.etNameProfile = Entry(self.frameNameProfile, width=50, font=self.fontInputs, disabledforeground='black')
        self.etNameProfile.grid()

        # Office
        self.frameOfficeProfile = Frame(self.frameServProfile, bg=self.bg, padx=10, pady=10)
        self.frameOfficeProfile.grid()

        self.lbOfficeProfile = Label(self.frameOfficeProfile, bg=self.bg, font=self.font, text='Cargo:')
        self.lbOfficeProfile['font'] = self.font
        self.lbOfficeProfile.grid(sticky=W)

        self.etOfficeProfile = Entry(self.frameOfficeProfile, font=self.fontInputs, width=50,
                                     disabledforeground='black')
        self.etOfficeProfile.grid()

        # Current Sector
        self.frameDepartamentProfile = Frame(self.frameServProfile, bg=self.bg, padx=10, pady=10)
        self.frameDepartamentProfile.grid()

        self.lbDepartamentProfile = Label(self.frameDepartamentProfile, bg=self.bg, font=self.font, text='Setor atual:')
        self.lbDepartamentProfile.grid(sticky=W)

        self.etDepartamentProfile = Entry(self.frameDepartamentProfile, width=50, font=self.fontInputs,
                                          disabledforeground='black')
        self.etDepartamentProfile.grid()

        # Reason
        self.frameReasonProfile = Frame(self.frameServProfile, bg=self.bg, padx=10, pady=10)
        self.frameReasonProfile.grid()

        self.lbReasonProfile = Label(self.frameReasonProfile, bg=self.bg, font=self.font, text='Motivo do afastamento:')
        self.lbReasonProfile.grid(row=0, sticky=W)

        self.etReasonProfile = Entry(self.frameReasonProfile, width=50, font=self.fontInputs,
                                     disabledforeground='black')
        self.etReasonProfile.grid(row=1)

        # Contact
        self.frameContactProfile = Frame(self.frameReasonProfile, bg=self.bg, pady=5)
        self.frameContactProfile.grid(row=2, sticky=W)

        self.lbContactProfile = Label(self.frameContactProfile, bg=self.bg, font=self.font, text='Contato:')
        self.lbContactProfile.grid(sticky=W)

        # Type
        self.frameTypeProfile = Frame(self.frameReasonProfile, bg=self.bg, pady=10)
        self.frameTypeProfile.grid(row=2, sticky=E)

        self.lbtypeProfile = Label(self.frameTypeProfile, bg=self.bg, font=self.font, text='Tipo:')
        self.lbtypeProfile.grid(row=1, column=2, sticky=W)

        self.TypeProfile = None

        self.varHuProfile = IntVar()
        self.btHuProfile = Checkbutton(self.frameTypeProfile, text='HU', bg=self.bg, font=self.font2,
                                       variable=self.varHuProfile)
        self.btHuProfile['command'] = partial(self.checkTypeProfile, self.btHuProfile)
        self.btHuProfile.grid(row=2, column=3)

        self.varUfmaProfile = IntVar()
        self.btUfmaProfile = Checkbutton(self.frameTypeProfile, text='UFMA', bg=self.bg, font=self.font2,
                                         variable=self.varUfmaProfile)
        self.btUfmaProfile['command'] = partial(self.checkTypeProfile, self.btUfmaProfile)
        self.btUfmaProfile.grid(row=2, column=2)

        # Process container
        self.frameNumProcessProfile = Frame(self.frameServProfile, bg=self.bg)
        self.frameNumProcessProfile.grid(pady=5)

        self.frameNprocessProfile = Frame(self.frameServProfile, bg=self.bg)
        self.frameNprocessProfile.grid(sticky=W, pady=5)

        self.lbNprocessProfile = Label(self.frameNumProcessProfile, text='Número do processo:', bg=self.bg,
                                       font=self.font, pady=10)
        self.lbNprocessProfile.grid(sticky=W)

        # Process type
        self.lbType_processProfile = Label(self.frameNprocessProfile, text='Tipo do processo:', bg=self.bg,
                                           font=self.font)
        self.lbType_processProfile.grid(sticky=W)

        self.type_proProfile = None

        self.varAclProfile = IntVar()
        self.checkLcaProfile = Checkbutton(self.frameNprocessProfile, text='Avaliação da Capacidade Laboral',
                                           bg=self.bg,
                                           font=self.font2, variable=self.varAclProfile)
        self.checkLcaProfile.grid(sticky=W)
        self.checkLcaProfile['command'] = partial(self.checkTypeProProfile, self.checkLcaProfile)

        self.varRaProfile = IntVar()
        self.checkRaProfile = Checkbutton(self.frameNprocessProfile, text='Restrição de atividades', bg=self.bg,
                                          font=self.font2,
                                          variable=self.varRaProfile)
        self.checkRaProfile.grid(sticky=W)
        self.checkRaProfile['command'] = partial(self.checkTypeProProfile, self.checkRaProfile)

        self.varRProfile = IntVar()
        self.checkRProfile = Checkbutton(self.frameNprocessProfile, text='Readaptação', bg=self.bg, font=self.font2,
                                         variable=self.varRProfile)
        self.checkRProfile.grid(sticky=W)
        self.checkRProfile['command'] = partial(self.checkTypeProProfile, self.checkRProfile)

        # Dates
        self.frameDateButtonsProfile = Frame(self.Profile, bg=self.bg)
        self.frameDateButtonsProfile.grid(row=1, column=2, sticky=NW, padx=5)

        self.frameDateProfile = Frame(self.frameDateButtonsProfile, relief=GROOVE, borderwidth=2)
        self.frameDateProfile.grid(sticky=N)

        # Biannually
        self.frameBiProfile = Frame(self.frameDateProfile, bg=self.bg, padx=50, pady=10)
        self.frameBiProfile.pack(fill='x')

        self.lbBiProfile = Label(self.frameBiProfile, bg=self.bg, font=self.font, text='Avaliação da perícia:')
        self.lbBiProfile.grid()

        self.lbLd_BiProfile = Label(self.frameBiProfile, bg=self.bg, font=self.font, text='Última avaliação:')
        self.lbLd_BiProfile.grid(row=1, sticky=W)

        self.lbNd_BiProfile = Label(self.frameBiProfile, bg=self.bg, font=self.font, text='Próxima avaliação:')
        self.lbNd_BiProfile.grid(row=3, sticky=W)

        # Quarterly
        self.frameQuaProfile = Frame(self.frameDateProfile, bg=self.bg, padx=50, pady=10)
        self.frameQuaProfile.pack(fill='x')

        self.lbQuaProfile = Label(self.frameQuaProfile, bg=self.bg, font=self.font, text='Avaliação do Readaptar:')
        self.lbQuaProfile.grid()

        self.lbLd_QuaProfile = Label(self.frameQuaProfile, bg=self.bg, font=self.font, text='Última avaliação:')
        self.lbLd_QuaProfile.grid(row=1, sticky=W)

        self.lbNd_QuaProfile = Label(self.frameQuaProfile, bg=self.bg, font=self.font, text='Próxima avaliação:')
        self.lbNd_QuaProfile.grid(row=3, sticky=W)

        # Buttons Save e Back
        self.frameButtonsProfile = Frame(self.Profile, bg=self.bg, pady=50)
        self.frameButtonsProfile.grid(row=1, column=3, padx=90)

        self.editProfile = Button(self.frameButtonsProfile, text='Editar', bg=self.bgButtonR, font=self.fontButton,
                                  fg=self.fgButton, width=15, command=self.editingProfile)
        self.editProfile.pack(pady=5, padx=10)

        self.excludeProfile = Button(self.frameButtonsProfile, text='Excluir', bg=self.bgButtonR, font=self.fontButton,
                                     fg=self.fgButton, width=15, command=self.excludeServerProfile)
        self.excludeProfile.pack(pady=5, padx=10)

        self.backProfile = Button(self.frameButtonsProfile, text='Voltar', bg=self.bgButtonR, font=self.fontButton,
                                  fg=self.fgButton, width=15, command=self.profileToMain)
        self.backProfile.pack(pady=5, padx=10)

        self.frameButtonsEditing = Frame(self.Profile, bg=self.bg, pady=50)

        self.saveEditing = Button(self.frameButtonsEditing, text='Salvar Alterações', bg=self.bgButtonG,
                                  font=self.fontButton, fg=self.fgButton, width=25, command=self.updateServers)
        self.saveEditing.pack(pady=5)

        self.CancelEditing = Button(self.frameButtonsEditing, text='Cancelar', bg=self.bgButtonR, font=self.fontButton,
                                    fg=self.fgButton, width=15, command=self.cancelEditing)
        self.CancelEditing.pack(pady=5)

        # Remarks
        self.frameRemarkProfile = Frame(self.Profile, bg=self.bg, relief=GROOVE, borderwidth=2)
        self.frameRemarkProfile.grid(row=2, columnspan=2, column=2, sticky=NW, padx=5)

        self.treeRemarkHeadProfile = ("Atualizações", 'data')
        self.remarksProfile = []

        self.frameTreeRemarkProfile = Frame(self.frameRemarkProfile, bg=self.bg)
        self.frameTreeRemarkProfile.grid(padx=5, pady=5)

        self.treeRemarkProfile = ttk.Treeview(columns=self.treeRemarkHeadProfile, show="headings", height=11)
        self.sbRemarkProfile = ttk.Scrollbar(orient="vertical", command=self.treeRemarkProfile.yview)
        self.treeRemarkProfile.configure(yscrollcommand=self.sbRemarkProfile.set)
        self.treeRemarkProfile.grid(in_=self.frameTreeRemarkProfile)
        self.sbRemarkProfile.grid(column=1, row=0, sticky='ns', in_=self.frameTreeRemarkProfile)
        self.treeRemarkProfile.bind("<<TreeviewSelect>>", self.on_mainTreeRemark_select1Profile)
        self.treeRemarkProfile.bind("<Double-Button-1>", self.on_mainTreeRemark_select2Profile)

        for col in self.treeRemarkHeadProfile:
            self.treeRemarkProfile.heading(col, text=col.title())
        self.treeRemarkProfile.column(0, width=180)
        self.treeRemarkProfile.column(1, width=110)

        self.frameInsertRemarkProfile = Frame(self.frameRemarkProfile, bg=self.bg, pady=50)

        self.insertRemarkProfile = Button(self.frameInsertRemarkProfile, text='Inserir observação', bg=self.bgButtonG,
                                          font=self.fontButton, fg=self.fgButton, width=25,
                                          command=self.newRemarkProfile)
        self.insertRemarkProfile.grid(pady=5)

        self.window = None
        self.windowProfile = None
        self.remarkSelected = None
        self.remarkSelectedProfile = None
        self.checkEdit = False
        self.note = None

    def checkType(self, bt):
        # Control the Checkbuttons' server type
        if bt['text'] == 'HU' and self.Type == 0:
            self.Type = None
        elif bt['text'] == 'UFMA' and self.Type == 1:
            self.Type = None
        elif bt['text'] == 'HU' and self.Type != 0:
            self.Type = 0
            self.varUfma.set(0)
        elif bt['text'] == 'UFMA' and self.Type != 1:
            self.Type = 1
            self.varHu.set(0)

    def checkTypePro(self, bt):
        # Control the Checkbuttons' type of process
        if bt['text'] == 'Avaliação da Capacidade Laboral' and self.type_pro == 'Avaliação da Capacidade Laboral':
            self.type_pro = None
        elif bt['text'] == 'Restrição de atividades' and self.type_pro == 'Restrição de atividades':
            self.type_pro = None
        elif bt['text'] == 'Readaptação' and self.type_pro == 'Readaptação':
            self.type_pro = None
        elif bt['text'] == 'Avaliação da Capacidade Laboral' and self.type_pro != 'Avaliação da Capacidade Laboral':
            self.type_pro = 'Avaliação da Capacidade Laboral'
            self.varR.set(0)
            self.varRa.set(0)
        elif bt['text'] == 'Restrição de atividades' and self.type_pro != 'Restrição de atividades':
            self.type_pro = 'Restrição de atividades'
            self.varAcl.set(0)
            self.varR.set(0)
        elif bt['text'] == 'Readaptação' and self.type_pro != 'Readaptação':
            self.type_pro = 'Readaptação'
            self.varAcl.set(0)
            self.varRa.set(0)

    def checkClassification(self, bt):
        self.etSearch.delete(0, END)
        if bt['text'] == 'T0D0S' and str(self.varClassific) == str(None):
            self.varClassificAll.set(1)
        elif bt['text'] == 'HU' and self.varClassific == 0:
            self.varClassificHu.set(1)
        elif bt['text'] == 'UFMA' and self.varClassific == 1:
            self.varClassificUfma.set(1)
        elif bt['text'] == 'TODOS' and self.varClassific != None:
            self.varClassific = None
            self.varClassificHu.set(0)
            self.varClassificUfma.set(0)
            self.verify = True
            self.loadServersTree(self.varClassific)
        elif bt['text'] == 'HU' and self.varClassific != 0:
            self.varClassific = 0
            self.varClassificAll.set(0)
            self.varClassificUfma.set(0)
            self.verify = True
            self.loadServersTree(self.varClassific)
        elif bt['text'] == 'UFMA' and self.varClassific != 1:
            self.varClassific = 1
            self.varClassificAll.set(0)
            self.varClassificHu.set(0)
            self.verify = True
            self.loadServersTree(self.varClassific)

    def insertServers(self):
        # Put the servers' data on the server object to insert on DataBase
        server = Server()
        name, office, departament = self.etName.get(), self.etOffice.get(), self.etDepartament.get()
        reason, process, contact, bild = self.etReason.get(), self.etProcess.get(), self.etContact.get(), self.etLd_Bi.get()
        bind, quald, quand = self.etNd_Bi.get(), self.etLd_Qua.get(), self.etNd_Qua.get()
        if ((self.checkDatePass(bild) == True or self.checkDatePass(bild) == None) and (
                self.checkDatePass(bind) == False or self.checkDatePass(bind) == None)) or (
                (self.checkDatePass(quald) == True or self.checkDatePass(quald) == None) and (
                self.checkDatePass(quand) == False or self.checkDatePass(quand) == None)):
            if name != '' and office != '' and departament != '' and reason != '' and process != '' and bild != '' and bind != '':
                server.set_name(name)
                server.set_office(office)
                server.set_departament(departament)
                server.set_reason(reason)
                server.set_process(process)
                server.set_type_process(self.type_pro)
                server.set_contact(contact)
                server.set_type_number(self.Type)
                server.set_biannually_ld(ajustDate(bild))
                server.set_biannually_nd(ajustDate(bind))
                server.set_quarterly_ld(ajustDate(quald))
                server.set_quarterly_nd(ajustDate(quand))
                server.set_delete(1)
                server.set_evaluate_date(evaluateDate(server))
                try:
                    insertServer(server, self.remarks)
                except:
                    messagebox.showinfo('Erro', 'Erro!')
                self.cleanInsert()
                self.frameInsert.pack_forget()
                self.frameMain.pack(fill='both', expand=True)
                self.loadServersTree(self.varClassific)
            else:
                message = messagebox.showinfo('Atenção', 'Preencha todos os campos!')
        else:
            message = messagebox.showinfo('Atenção',
                                          'As últimas datas de avaliações devem ser anteriores ao dia de hoje e as próximas devem ser posteriores.')

    def cleanInsert(self):
        self.etName.delete(0, END)
        self.etOffice.delete(0, END)
        self.etProcess.destroy()
        self.etContact.destroy()
        self.etReason.delete(0, END)
        self.etDepartament.delete(0, END)
        self.etLd_Qua.destroy()
        self.etLd_Bi.destroy()
        self.etNd_Bi.destroy()
        self.etNd_Qua.destroy()
        # self.newEntryField.delete(1.0,END)
        self.varUfma.set(0)
        self.varHu.set(0)
        self.varRa.set(0)
        self.varR.set(0)
        self.varAcl.set(0)
        self.type_pro, self.Type = None, None
        self.treeRemark.delete(*self.treeRemark.get_children())
        # self.frameNewEntry.grid_forget()
        # self.frameInsertRemark.grid()

    def loadServersTree(self, type):
        # Load the servers data to show on main screen
        if self.varClassific == None:
            self.varClassificAll.set(1)
        elif self.varClassific == 0:
            self.varClassificHu.set(1)
        elif self.varClassific == 1:
            self.varClassificUfma.set(1)
        tree_data = getMainDataServers(type)
        # if self.verify==True:
        self.treeServers.delete(*self.treeServers.get_children())
        for item in tree_data:
            self.treeServers.insert('', 'end', values=item[:6])
        return tree_data

    def mainToInsert(self):
        # Show the insert page
        self.frameMain.pack_forget()
        self.etContact = MaskedWidget(self.frameContact, 'fixed', mask='(99) 99999-9999', width=20,
                                      font=self.fontInputs)
        self.etContact.grid()
        self.etProcess = MaskedWidget(self.frameNumProcess, 'fixed', mask='99999.999999/9999-99', width=50,
                                      font=self.fontInputs)
        self.etProcess.grid()
        self.etLd_Bi = MaskedWidget(self.frameBi, 'fixed', mask='99/99/9999', width=20, font=self.fontInputs)
        self.etLd_Bi.grid(row=2, sticky=W)
        self.etNd_Bi = MaskedWidget(self.frameBi, 'fixed', mask='99/99/9999', width=20, font=self.fontInputs)
        self.etNd_Bi.grid(row=4, sticky=W)
        self.etLd_Qua = MaskedWidget(self.frameQua, 'fixed', mask='99/99/9999', width=20, font=self.fontInputs)
        self.etLd_Qua.grid(row=2, sticky=W)
        self.etNd_Qua = MaskedWidget(self.frameQua, 'fixed', mask='99/99/9999', width=20, font=self.fontInputs)
        self.etNd_Qua.grid(row=4, sticky=W)
        self.frameInsert.pack(side=TOP, anchor=CENTER)
        self.varClassific = None
        # self.verify=False

    def insertToMain(self):
        # Return to main screen updating
        self.cleanInsert()
        self.loadServersTree(self.varClassific)
        self.frameMain.pack(fill='both', expand=True)
        self.frameInsert.pack_forget()
        self.remarks = []
        self.serverSelected = None

    def newRemark(self):
        if self.window != None:
            self.window.destroy()
        remarkNumber = str(len(self.remarks) + 1)
        self.window = Toplevel(self.frameInsert)
        self.window.geometry('400x400+150+200')
        self.window.title('Nova Observação')
        self.frameNewRemarkWindow = Frame(self.window)
        self.frameNewRemarkWindow.pack()
        self.lbTitleRemarkWindow = Label(self.frameNewRemarkWindow, text='Título:', font=self.font)
        self.lbTitleRemarkWindow.grid(sticky=W)
        self.etTitleRemarkWindow = Entry(self.frameNewRemarkWindow, width=35, font=self.fontInputs)
        self.etTitleRemarkWindow.insert(0, 'Observação %s' % (remarkNumber))
        self.etTitleRemarkWindow.grid(sticky=W)
        self.lbDateRemarkWindow = Label(self.frameNewRemarkWindow, text='Data:', font=self.font)
        self.lbDateRemarkWindow.grid(sticky=W)
        self.etDateRemarkWindow = MaskedWidget(self.frameNewRemarkWindow, 'fixed', mask='99/99/9999', width=15,
                                               font=self.fontInputs, disabledforeground='black')
        self.etDateRemarkWindow.insert(0, datetime.now().strftime('%d%m%Y'))
        self.etDateRemarkWindow['state'] = DISABLED
        self.etDateRemarkWindow.grid(sticky=W)
        self.lbNewRemarkWindow = Label(self.frameNewRemarkWindow, text='Observação:', font=self.font)
        self.lbNewRemarkWindow.grid(sticky=W)
        self.frameRemarkWindow = Frame(self.frameNewRemarkWindow, bg=self.bg)
        self.frameRemarkWindow.grid(sticky=W)
        self.etNewRemarkWindow = Text(self.frameRemarkWindow, width=35, height=10, font=self.fontInputs)
        self.etNewRemarkWindow.pack(side=LEFT)
        self.scrolNewremarkWindow = Scrollbar(self.frameRemarkWindow, command=self.etNewRemarkWindow.yview)
        self.etNewRemarkWindow['yscrollcommand'] = self.scrolNewremarkWindow.set
        self.scrolNewremarkWindow.pack(side=RIGHT, fill='y')
        self.btInsertRemarkWindow = Button(self.frameNewRemarkWindow, text='Salvar', bg=self.bgButtonG,
                                           fg=self.fgButton, font=self.fontButton, command=self.putRemark)
        self.btInsertRemarkWindow.grid(pady=20)

    def putRemark(self):
        value = str(self.etNewRemarkWindow.get(1.0, END))
        title = str(self.etTitleRemarkWindow.get())
        note = Remark()
        note.set_remark(value)
        note.set_about(title)
        self.remarks.append(note)
        self.loadTreeRemark()
        self.window.destroy()

    def viewRemark(self):
        if self.window != None:
            self.window.destroy()
        if self.remarkSelected != None:
            self.window = Toplevel(self.frameInsert)
            self.window.geometry('400x400+150+200')
            self.window.title('Observação')
            self.frameNewRemarkWindow = Frame(self.window)
            self.frameNewRemarkWindow.pack()
            self.lbTitleRemarkWindow = Label(self.frameNewRemarkWindow, text='Título:', font=self.font)
            self.lbTitleRemarkWindow.grid(sticky=W)
            self.etTitleRemarkWindow = Entry(self.frameNewRemarkWindow, width=35, font=self.fontInputs,
                                             disabledforeground='black')
            self.etTitleRemarkWindow.insert(0, '%s' % (self.remarks[self.remarkSelected].get_about()))
            self.etTitleRemarkWindow['state'] = DISABLED
            self.etTitleRemarkWindow.grid(sticky=W)
            self.frameDateRemarkWindow = Frame(self.frameNewRemarkWindow)
            self.frameDateRemarkWindow.grid(sticky=W)
            self.lbDateRemarkWindow = Label(self.frameDateRemarkWindow, text='Data:', font=self.font)
            self.lbDateRemarkWindow.grid(sticky=W)
            self.etDateRemarkWindow = MaskedWidget(self.frameDateRemarkWindow, 'fixed', mask='99/99/9999', width=15,
                                                   font=self.fontInputs, disabledforeground='black')
            self.etDateRemarkWindow.insert(0, '%s' % (
                reajustDate(cleanData(self.remarks[self.remarkSelected].get_time()))))
            self.etDateRemarkWindow['state'] = DISABLED
            self.etDateRemarkWindow.grid(sticky=W)
            self.lbNewRemarkWindow = Label(self.frameNewRemarkWindow, text='Observação:', font=self.font)
            self.lbNewRemarkWindow.grid(sticky=W)
            self.frameRemarkWindow = Frame(self.frameNewRemarkWindow, bg=self.bg)
            self.frameRemarkWindow.grid(sticky=W)
            self.etNewRemarkWindow = Text(self.frameRemarkWindow, width=35, height=10, font=self.fontInputs)
            self.etNewRemarkWindow.insert(1.0, '%s' % (self.remarks[self.remarkSelected].get_remark()))
            self.etNewRemarkWindow['state'] = DISABLED
            self.etNewRemarkWindow.pack(side=LEFT)
            self.scrolNewremarkWindow = Scrollbar(self.frameRemarkWindow, command=self.etNewRemarkWindow.yview)
            self.etNewRemarkWindow['yscrollcommand'] = self.scrolNewremarkWindow.set
            self.scrolNewremarkWindow.pack(side=RIGHT, fill='y')
            self.frameButtonsEditRemark = Frame(self.frameNewRemarkWindow, bg=self.bg)
            self.btSaveRemarkWindow = Button(self.frameButtonsEditRemark, text='Salvar', bg=self.bgButtonG,
                                             fg=self.fgButton, font=self.fontButton, command=self.updateRemark)
            self.btSaveRemarkWindow.grid(padx=5)
            self.btCancelRemarkWindow = Button(self.frameButtonsEditRemark, text='Cancelar', bg=self.bgButtonR,
                                               fg=self.fgButton, font=self.fontButton, command=self.cancelEditingRemark)
            self.btCancelRemarkWindow.grid(row=0, column=1, padx=5)
            self.frameButtonsRemark = Frame(self.frameNewRemarkWindow, bg=self.bg)
            self.frameButtonsRemark.grid(pady=20)
            self.btInsertRemarkWindow = Button(self.frameButtonsRemark, text='Editar', bg=self.bgButtonG,
                                               fg=self.fgButton, font=self.fontButton, command=self.editingRemark)
            self.btInsertRemarkWindow.grid(padx=5)
            self.btDelRemarkWindow = Button(self.frameButtonsRemark, text='Deletar', bg=self.bgButtonG,
                                            fg=self.fgButton, font=self.fontButton, command=self.deleteRemark)
            self.btDelRemarkWindow.grid(row=0, column=1, padx=5)

    def editingRemark(self):
        self.etTitleRemarkWindow['state'] = NORMAL
        self.etNewRemarkWindow['state'] = NORMAL
        self.frameButtonsRemark.grid_forget()
        self.frameButtonsEditRemark.grid(pady=20)

    def cancelEditingRemark(self):
        self.etTitleRemarkWindow.delete(0, END)
        self.etNewRemarkWindow.delete(1.0, END)
        self.etTitleRemarkWindow.insert(0, '%s' % (self.remarks[self.remarkSelected].get_about()))
        self.etTitleRemarkWindow['state'] = DISABLED
        self.etNewRemarkWindow.insert(1.0, '%s' % (self.remarks[self.remarkSelected].get_remark()))
        self.etNewRemarkWindow['state'] = DISABLED
        self.frameButtonsEditRemark.grid_forget()
        self.frameButtonsRemark.grid(pady=20)
        self.check = False

    def updateRemark(self):
        value = self.etNewRemarkWindow.get(1.0, END)
        title = self.etTitleRemarkWindow.get()
        self.remarks[self.remarkSelected].set_about(title)
        self.remarks[self.remarkSelected].set_remark(value)
        self.loadTreeRemark()
        self.window.destroy()

    def deleteRemark(self):
        lixo = self.remarks.pop(self.remarkSelected)
        self.loadTreeRemark()
        self.window.destroy()

    def loadTreeRemark(self):
        self.treeRemark.delete(*self.treeRemark.get_children())
        if self.remarks != None:
            for item in self.remarks:
                self.treeRemark.insert('', 'end',
                                       values=[item.get_about(), reajustDateForMain(cleanData(item.get_time()))])

    def mainToProfile(self):
        # Show the Profile page
        if self.serverSelected != None:
            self.frameMain.pack_forget()
            self.Profile.pack(side=TOP, anchor=CENTER, padx=70)
            self.server = getServer(self.serverSelected)
            self.server.set_id(self.serverSelected)
            self.etNameProfile.insert(0, self.server.get_name())
            self.etNameProfile['state'] = DISABLED
            self.etOfficeProfile.insert(0, self.server.get_office())
            self.etOfficeProfile['state'] = DISABLED
            self.etDepartamentProfile.insert(0, self.server.get_departament())
            self.etDepartamentProfile['state'] = DISABLED
            self.etReasonProfile.insert(0, self.server.get_reason())
            self.etReasonProfile['state'] = DISABLED
            self.etProcessProfile = MaskedWidget(self.frameNumProcessProfile, 'fixed', mask='99999.999999/9999-99',
                                                 width=50, font=self.fontInputs, disabledforeground='black')
            self.etProcessProfile.grid()
            self.etProcessProfile.insert(0, cleanData(self.server.get_process()))
            self.etProcessProfile['state'] = DISABLED
            self.etContactProfile = MaskedWidget(self.frameContactProfile, 'fixed', mask='(99) 99999-9999', bg=self.bg,
                                                 width=20, font=self.fontInputs, disabledforeground='black')
            self.etContactProfile.grid()
            self.etContactProfile.insert(0, cleanData(self.server.get_contact()))
            self.etContactProfile['state'] = DISABLED
            self.etLd_BiProfile = MaskedWidget(self.frameBiProfile, 'fixed', mask='99/99/9999', width=20,
                                               font=self.fontInputs, disabledforeground='black')
            self.etLd_BiProfile.grid(row=2, sticky=W)
            self.etLd_BiProfile.insert(0, reajustDate(cleanData(self.server.get_biannually_ld())))
            self.etLd_BiProfile['state'] = DISABLED
            self.etNd_BiProfile = MaskedWidget(self.frameBiProfile, 'fixed', mask='99/99/9999', width=20,
                                               font=self.fontInputs, disabledforeground='black')
            self.etNd_BiProfile.grid(row=4, sticky=W)
            self.etNd_BiProfile.insert(0, reajustDate(cleanData(self.server.get_biannually_nd())))
            self.etNd_BiProfile['state'] = DISABLED
            self.etLd_QuaProfile = MaskedWidget(self.frameQuaProfile, 'fixed', mask='99/99/9999', width=20,
                                                font=self.fontInputs, disabledforeground='black')
            self.etLd_QuaProfile.grid(row=2, sticky=W)
            self.etLd_QuaProfile.insert(0, reajustDate(cleanData(self.server.get_quarterly_ld())))
            self.etLd_QuaProfile['state'] = DISABLED
            self.etNd_QuaProfile = MaskedWidget(self.frameQuaProfile, 'fixed', mask='99/99/9999', width=20,
                                                font=self.fontInputs, disabledforeground='black')
            self.etNd_QuaProfile.grid(row=4, sticky=W)
            self.etNd_QuaProfile.insert(0, reajustDate(cleanData(self.server.get_quarterly_nd())))
            self.etNd_QuaProfile['state'] = DISABLED
            self.type_proProfile = self.server.get_type_process()
            if self.server.get_type_process() == 'Avaliação da Capacidade Laboral':
                self.varAclProfile.set(1)
                self.checkLcaProfile['state'] = DISABLED
                self.checkRaProfile['state'] = DISABLED
                self.checkRProfile['state'] = DISABLED
            elif self.server.get_type_process() == 'Restrição de atividades':
                self.varRaProfile.set(1)
                self.checkLcaProfile['state'] = DISABLED
                self.checkRaProfile['state'] = DISABLED
                self.checkRProfile['state'] = DISABLED
            elif self.server.get_type_process() == 'Readaptação':
                self.varRProfile.set(1)
                self.checkLcaProfile['state'] = DISABLED
                self.checkRaProfile['state'] = DISABLED
                self.checkRProfile['state'] = DISABLED
            self.TypeProfile = self.server.get_type_number()
            if self.server.get_type_number() == 1:
                self.varUfmaProfile.set(1)
                self.btHuProfile['state'] = DISABLED
                self.btUfmaProfile['state'] = DISABLED
            elif self.server.get_type_number() == 0:
                self.varHuProfile.set(1)
                self.btHuProfile['state'] = DISABLED
                self.btUfmaProfile['state'] = DISABLED
            self.remarksProfile = getRemark(self.server.get_id())
            self.loadTreeRemarkProfile()
        else:
            self.messageInsert = messagebox.showinfo('', 'Selecione um servidor!')

    def cleanProfile(self):
        self.etNameProfile.delete(0, END)
        self.etOfficeProfile.delete(0, END)
        self.etProcessProfile.destroy()
        self.etContactProfile.destroy()
        self.etReasonProfile.delete(0, END)
        self.etDepartamentProfile.delete(0, END)
        self.etLd_QuaProfile.destroy()
        self.etLd_BiProfile.destroy()
        self.etNd_BiProfile.destroy()
        self.etNd_QuaProfile.destroy()
        self.varUfmaProfile.set(0)
        self.varHuProfile.set(0)
        self.varRaProfile.set(0)
        self.varRProfile.set(0)
        self.varAclProfile.set(0)
        self.type_proProfile, self.TypeProfile = None, None
        self.treeRemarkProfile.delete(*self.treeRemarkProfile.get_children())

    def profileToMain(self):
        # Return to main screen updating
        self.loadServersTree(self.varClassific)
        self.frameMain.pack(fill='both', expand=True)
        self.Profile.pack_forget()
        self.etNameProfile['state'] = NORMAL
        self.etOfficeProfile['state'] = NORMAL
        self.etDepartamentProfile['state'] = NORMAL
        self.etReasonProfile['state'] = NORMAL
        self.checkLcaProfile['state'] = NORMAL
        self.checkRaProfile['state'] = NORMAL
        self.checkRProfile['state'] = NORMAL
        self.btUfmaProfile['state'] = NORMAL
        self.btHuProfile['state'] = NORMAL
        self.cleanProfile()
        self.server = None
        self.remarksProfile = []
        self.serverSelected = None

    def checkTypeProfile(self, bt):
        # Control the Checkbuttons' server type
        if bt['text'] == 'HU' and self.TypeProfile == 0:
            self.TypeProfile = None
            self.lbtypeProfile['text'] = 'nada'
        elif bt['text'] == 'UFMA' and self.TypeProfile == 1:
            self.TypeProfile = None
            self.lbtypeProfile['text'] = 'nada'
        elif bt['text'] == 'HU' and self.TypeProfile != 0:
            self.TypeProfile = 0
            self.lbtypeProfile['text'] = 'hu'
            self.varUfmaProfile.set(0)
        elif bt['text'] == 'UFMA' and self.TypeProfile != 1:
            self.TypeProfile = 1
            self.lbtypeProfile['text'] = 'ufma'
            self.varHuProfile.set(0)

    def checkTypeProProfile(self, bt):
        # Control the Checkbuttons' type of process
        if bt[
            'text'] == 'Avaliação da Capacidade Laboral' and self.type_proProfile == 'Avaliação da Capacidade Laboral':
            self.type_proProfile = None
            self.lbType_processProfile['text'] = 'nada'
        elif bt['text'] == 'Restrição de atividades' and self.type_proProfile == 'Restrição de atividades':
            self.type_proProfile = None
            self.lbType_processProfile['text'] = 'nada'
        elif bt['text'] == 'Readaptação' and self.type_proProfile == 'Readaptação':
            self.type_proProfile = None
            self.lbType_processProfile['text'] = 'nada'
        elif bt[
            'text'] == 'Avaliação da Capacidade Laboral' and self.type_proProfile != 'Avaliação da Capacidade Laboral':
            self.type_proProfile = 'Avaliação da Capacidade Laboral'
            self.lbType_processProfile['text'] = self.type_proProfile
            self.varRProfile.set(0)
            self.varRaProfile.set(0)
        elif bt['text'] == 'Restrição de atividades' and self.type_proProfile != 'Restrição de atividades':
            self.type_proProfile = 'Restrição de atividades'
            self.lbType_processProfile['text'] = self.type_proProfile
            self.varAclProfile.set(0)
            self.varRProfile.set(0)
        elif bt['text'] == 'Readaptação' and self.type_proProfile != 'Readaptação':
            self.type_proProfile = 'Readaptação'
            self.lbType_processProfile['text'] = self.type_proProfile
            self.varAclProfile.set(0)
            self.varRaProfile.set(0)

    def editingProfile(self):
        self.etNameProfile['state'] = NORMAL
        self.etOfficeProfile['state'] = NORMAL
        self.etDepartamentProfile['state'] = NORMAL
        self.etReasonProfile['state'] = NORMAL
        self.etProcessProfile['state'] = NORMAL
        self.etContactProfile['state'] = NORMAL
        self.etLd_BiProfile['state'] = NORMAL
        self.etNd_BiProfile['state'] = NORMAL
        self.etLd_QuaProfile['state'] = NORMAL
        self.etNd_QuaProfile['state'] = NORMAL
        self.checkLcaProfile['state'] = NORMAL
        self.checkRaProfile['state'] = NORMAL
        self.checkRProfile['state'] = NORMAL
        self.btUfmaProfile['state'] = NORMAL
        self.btHuProfile['state'] = NORMAL
        self.frameButtonsProfile.grid_forget()
        self.checkEdit = True
        self.frameButtonsEditing.grid(row=1, column=3, padx=90)
        self.frameInsertRemarkProfile.grid(row=0, column=3, padx=50)

    def cancelEditing(self):
        self.cleanProfile()
        self.frameButtonsEditing.grid_forget()
        self.frameInsertRemarkProfile.grid_forget()
        self.etNameProfile.insert(0, self.server.get_name())
        self.etNameProfile['state'] = DISABLED
        self.etOfficeProfile.insert(0, self.server.get_office())
        self.etOfficeProfile['state'] = DISABLED
        self.etDepartamentProfile.insert(0, self.server.get_departament())
        self.etDepartamentProfile['state'] = DISABLED
        self.etReasonProfile.insert(0, self.server.get_reason())
        self.etReasonProfile['bg'] = 'white'
        self.etReasonProfile['state'] = DISABLED
        self.etProcessProfile = MaskedWidget(self.frameNumProcessProfile, 'fixed', mask='99999.999999/9999-99',
                                             width=50, font=30, disabledforeground='black')
        self.etProcessProfile.grid()
        self.etProcessProfile.insert(0, cleanData(self.server.get_process()))
        self.etProcessProfile['state'] = DISABLED
        self.etContactProfile = MaskedWidget(self.frameContactProfile, 'fixed', mask='(99) 99999-9999', bg=self.bg,
                                             width=20, font=30, disabledforeground='black')
        self.etContactProfile.grid()
        self.etContactProfile.insert(0, cleanData(self.server.get_contact()))
        self.etContactProfile['state'] = DISABLED
        self.etLd_BiProfile = MaskedWidget(self.frameBiProfile, 'fixed', mask='99/99/9999', width=20, font=30,
                                           disabledforeground='black')
        self.etLd_BiProfile.grid(row=2, sticky=W)
        self.etLd_BiProfile.insert(0, reajustDate(cleanData(self.server.get_biannually_ld())))
        self.etLd_BiProfile['state'] = DISABLED
        self.etNd_BiProfile = MaskedWidget(self.frameBiProfile, 'fixed', mask='99/99/9999', width=20, font=30,
                                           disabledforeground='black')
        self.etNd_BiProfile.grid(row=4, sticky=W)
        self.etNd_BiProfile.insert(0, reajustDate(cleanData(self.server.get_biannually_nd())))
        self.etNd_BiProfile['state'] = DISABLED
        self.etLd_QuaProfile = MaskedWidget(self.frameQuaProfile, 'fixed', mask='99/99/9999', width=20, font=30,
                                            disabledforeground='black')
        self.etLd_QuaProfile.grid(row=2, sticky=W)
        self.etLd_QuaProfile.insert(0, reajustDate(cleanData(self.server.get_quarterly_ld())))
        self.etLd_QuaProfile['state'] = DISABLED
        self.etNd_QuaProfile = MaskedWidget(self.frameQuaProfile, 'fixed', mask='99/99/9999', width=20, font=30,
                                            disabledforeground='black')
        self.etNd_QuaProfile.grid(row=4, sticky=W)
        self.etNd_QuaProfile.insert(0, reajustDate(cleanData(self.server.get_quarterly_nd())))
        self.etNd_QuaProfile['state'] = DISABLED
        self.type_proProfile = self.server.get_type_process()
        if self.server.get_type_process() == 'Avaliação da Capacidade Laboral':
            self.varAclProfile.set(1)
            self.checkLcaProfile['state'] = DISABLED
            self.checkRaProfile['state'] = DISABLED
            self.checkRProfile['state'] = DISABLED
        elif self.server.get_type_process() == 'Restrição de atividades':
            self.varRaProfile.set(1)
            self.checkLcaProfile['state'] = DISABLED
            self.checkRaProfile['state'] = DISABLED
            self.checkRProfile['state'] = DISABLED
        elif self.server.get_type_process() == 'Readaptação':
            self.varRProfile.set(1)
            self.checkLcaProfile['state'] = DISABLED
            self.checkRaProfile['state'] = DISABLED
            self.checkRProfile['state'] = DISABLED
        self.TypeProfile = self.server.get_type_number()
        if self.server.get_type_number() == 1:
            self.varUfmaProfile.set(1)
            self.btHuProfile['state'] = DISABLED
            self.btUfmaProfile['state'] = DISABLED
        elif self.server.get_type_number() == 0:
            self.varHuProfile.set(1)
            self.btHuProfile['state'] = DISABLED
            self.btUfmaProfile['state'] = DISABLED
        self.remarksProfile = getRemark(self.server.get_id())
        self.loadTreeRemarkProfile()
        self.frameButtonsProfile.grid(row=1, column=3, padx=90)
        self.frameButtonsEditing.grid_forget()
        self.checkEdit = False

    def newRemarkProfile(self):
        if self.windowProfile != None:
            self.windowProfile.destroy()
        remarkNumberProfile = str(len(self.remarksProfile) + 1)
        self.windowProfile = Toplevel(self.Profile)
        self.windowProfile.geometry('400x400+150+200')
        self.windowProfile.title('Nova Observação')
        self.frameNewRemarkWindowProfile = Frame(self.windowProfile)
        self.frameNewRemarkWindowProfile.pack()
        self.lbTitleRemarkWindowProfile = Label(self.frameNewRemarkWindowProfile, text='Título:', font=self.font)
        self.lbTitleRemarkWindowProfile.grid(sticky=W)
        self.etTitleRemarkWindowProfile = Entry(self.frameNewRemarkWindowProfile, width=35, font=self.fontInputs)
        self.etTitleRemarkWindowProfile.insert(0, 'Observação %s' % (remarkNumberProfile))
        self.etTitleRemarkWindowProfile.grid(sticky=W)
        self.lbDateRemarkWindowProfile = Label(self.frameNewRemarkWindowProfile, text='Data:', font=self.font)
        self.lbDateRemarkWindowProfile.grid(sticky=W)
        self.etDateRemarkWindowProfile = MaskedWidget(self.frameNewRemarkWindowProfile, 'fixed', mask='99/99/9999',
                                                      width=15, font=self.fontInputs, disabledforeground='black')
        self.etDateRemarkWindowProfile.insert(0, datetime.now().strftime('%d%m%Y'))
        self.etDateRemarkWindowProfile['state'] = DISABLED
        self.etDateRemarkWindowProfile.grid(sticky=W)
        self.lbNewRemarkWindowProfile = Label(self.frameNewRemarkWindowProfile, text='Observação:', font=self.font)
        self.lbNewRemarkWindowProfile.grid(sticky=W)
        self.frameRemarkWindowProfile = Frame(self.frameNewRemarkWindowProfile, bg=self.bg)
        self.frameRemarkWindowProfile.grid(sticky=W)
        self.etNewRemarkWindowProfile = Text(self.frameRemarkWindowProfile, width=35, height=10, font=self.fontInputs)
        self.etNewRemarkWindowProfile.pack(side=LEFT)
        self.scrolNewremarkWindowProfile = Scrollbar(self.frameRemarkWindowProfile,
                                                     command=self.etNewRemarkWindowProfile.yview)
        self.etNewRemarkWindowProfile['yscrollcommand'] = self.scrolNewremarkWindowProfile.set
        self.scrolNewremarkWindowProfile.pack(side=RIGHT, fill='y')
        self.btInsertRemarkWindowProfile = Button(self.frameNewRemarkWindowProfile, text='Salvar', bg=self.bgButtonG,
                                                  fg=self.fgButton, font=self.fontButton, command=self.putRemarkProfile)
        self.btInsertRemarkWindowProfile.grid(pady=20)

    def putRemarkProfile(self):
        value = str(self.etNewRemarkWindowProfile.get(1.0, END))
        title = str(self.etTitleRemarkWindowProfile.get())
        note = Remark()
        note.set_remark(value)
        note.set_about(title)
        self.remarksProfile.append(note)
        self.loadTreeRemarkProfile()
        self.windowProfile.destroy()

    def viewRemarkProfile(self):
        if self.windowProfile != None:
            self.windowProfile.destroy()
        if self.remarkSelectedProfile != None:
            self.windowProfile = Toplevel(self.Profile)
            self.windowProfile.geometry('400x400+150+200')
            self.windowProfile.title('Observação')
            self.frameNewRemarkWindowProfile = Frame(self.windowProfile)
            self.frameNewRemarkWindowProfile.pack()
            self.lbTitleRemarkWindowProfile = Label(self.frameNewRemarkWindowProfile, text='Título:', font=self.font)
            self.lbTitleRemarkWindowProfile.grid(sticky=W)
            self.etTitleRemarkWindowProfile = Entry(self.frameNewRemarkWindowProfile, width=35, font=self.fontInputs,
                                                    disabledforeground='black')
            self.etTitleRemarkWindowProfile.insert(0,
                                                   '%s' % (self.remarksProfile[self.remarkSelectedProfile].get_about()))
            self.etTitleRemarkWindowProfile['state'] = DISABLED
            self.etTitleRemarkWindowProfile.grid(sticky=W)
            self.frameDateRemarkWindowProfile = Frame(self.frameNewRemarkWindowProfile)
            self.frameDateRemarkWindowProfile.grid(sticky=W)
            self.lbDateRemarkWindowProfile = Label(self.frameDateRemarkWindowProfile, text='Data:', font=self.font)
            self.lbDateRemarkWindowProfile.grid(sticky=W)
            self.etDateRemarkWindowProfile = MaskedWidget(self.frameDateRemarkWindowProfile, 'fixed', mask='99/99/9999',
                                                          width=15, font=self.fontInputs, disabledforeground='black')
            self.etDateRemarkWindowProfile.insert(0, '%s' % (
                reajustDate(cleanData(self.remarksProfile[self.remarkSelectedProfile].get_time()))))
            self.etDateRemarkWindowProfile['state'] = DISABLED
            self.etDateRemarkWindowProfile.grid(sticky=W)
            self.lbNewRemarkWindowProfile = Label(self.frameNewRemarkWindowProfile, text='Observação:', font=self.font)
            self.lbNewRemarkWindowProfile.grid(sticky=W)
            self.frameRemarkWindowProfile = Frame(self.frameNewRemarkWindowProfile, bg=self.bg)
            self.frameRemarkWindowProfile.grid(sticky=W)
            self.etNewRemarkWindowProfile = Text(self.frameRemarkWindowProfile, width=35, height=10,
                                                 font=self.fontInputs)
            self.etNewRemarkWindowProfile.insert(1.0,
                                                 '%s' % (self.remarksProfile[self.remarkSelectedProfile].get_remark()))
            self.etNewRemarkWindowProfile['state'] = DISABLED
            self.etNewRemarkWindowProfile.pack(side=LEFT)
            self.scrolNewremarkWindowProfile = Scrollbar(self.frameRemarkWindowProfile,
                                                         command=self.etNewRemarkWindowProfile.yview)
            self.etNewRemarkWindowProfile['yscrollcommand'] = self.scrolNewremarkWindowProfile.set
            self.scrolNewremarkWindowProfile.pack(side=RIGHT, fill='y')
            self.frameButtonsEditRemarkProfile = Frame(self.frameNewRemarkWindowProfile, bg=self.bg)
            self.btSaveRemarkWindowProfile = Button(self.frameButtonsEditRemarkProfile, text='Salvar',
                                                    bg=self.bgButtonG, fg=self.fgButton, font=self.fontButton,
                                                    command=self.updateRemarkProfile)
            self.btSaveRemarkWindowProfile.grid(padx=5)
            self.btCancelRemarkWindowProfile = Button(self.frameButtonsEditRemarkProfile, text='Cancelar',
                                                      bg=self.bgButtonR, fg=self.fgButton, font=self.fontButton,
                                                      command=self.cancelEditingRemarkProfile)
            self.btCancelRemarkWindowProfile.grid(row=0, column=1, padx=5)
            self.frameButtonsRemarkProfile = Frame(self.frameNewRemarkWindowProfile, bg=self.bg)
            if self.checkEdit == True:
                self.frameButtonsRemarkProfile.grid(pady=20)
            self.btInsertRemarkWindowProfile = Button(self.frameButtonsRemarkProfile, text='Editar', bg=self.bgButtonG,
                                                      fg=self.fgButton, font=self.fontButton,
                                                      command=self.editingRemarkProfile)
            self.btInsertRemarkWindowProfile.grid(padx=5)
            self.btDelRemarkWindowProfile = Button(self.frameButtonsRemarkProfile, text='Deletar', bg=self.bgButtonG,
                                                   fg=self.fgButton, font=self.fontButton,
                                                   command=self.deleteRemarkProfile)
            self.btDelRemarkWindowProfile.grid(row=0, column=1, padx=5)

    def editingRemarkProfile(self):
        self.etTitleRemarkWindowProfile['state'] = NORMAL
        self.etNewRemarkWindowProfile['state'] = NORMAL
        self.frameButtonsRemarkProfile.grid_forget()
        self.frameButtonsEditRemarkProfile.grid(pady=20)

    def cancelEditingRemarkProfile(self):
        self.etTitleRemarkWindowProfile.delete(0, END)
        self.etNewRemarkWindowProfile.delete(1.0, END)
        self.etTitleRemarkWindowProfile.insert(0, '%s' % (self.remarksProfile[self.remarkSelectedProfile].get_about()))
        self.etTitleRemarkWindowProfile['state'] = DISABLED
        self.etNewRemarkWindowProfile.insert(1.0, '%s' % (self.remarksProfile[self.remarkSelectedProfile].get_remark()))
        self.etNewRemarkWindowProfile['state'] = DISABLED
        self.frameButtonsEditRemarkProfile.grid_forget()
        self.frameButtonsRemarkProfile.grid(pady=20)

    def updateRemarkProfile(self):
        value = self.etNewRemarkWindowProfile.get(1.0, END)
        title = self.etTitleRemarkWindowProfile.get()
        if value != self.remarksProfile[self.remarkSelectedProfile].get_remark() + '\n' or title != self.remarksProfile[
            self.remarkSelectedProfile].get_about():
            self.remarksProfile[self.remarkSelectedProfile].change_edit()
        self.remarksProfile[self.remarkSelectedProfile].set_about(title)
        self.remarksProfile[self.remarkSelectedProfile].set_remark(value)
        self.loadTreeRemarkProfile()
        self.windowProfile.destroy()

    def deleteRemarkProfile(self):
        lixo = self.remarksProfile.pop(self.remarkSelectedProfile)
        self.loadTreeRemarkProfile()
        self.windowProfile.destroy()

    def loadTreeRemarkProfile(self):
        self.treeRemarkProfile.delete(*self.treeRemarkProfile.get_children())
        if self.remarksProfile != None:
            for item in self.remarksProfile:
                self.treeRemarkProfile.insert('', 'end',
                                              values=[item.get_about(), reajustDateForMain(cleanData(item.get_time()))])

    def updateServers(self):
        name, office, departament = self.etNameProfile.get(), self.etOfficeProfile.get(), self.etDepartamentProfile.get()
        reason, process, contact, bild = self.etReasonProfile.get(), self.etProcessProfile.get(), self.etContactProfile.get(), self.etLd_BiProfile.get()
        bind, quald, quand = self.etNd_BiProfile.get(), self.etLd_QuaProfile.get(), self.etNd_QuaProfile.get()
        if ((self.checkDatePass(bild) == True or self.checkDatePass(bild) == None) and (
                self.checkDatePass(quald) == True or self.checkDatePass(quald) == None)) or (
                (self.checkDatePass(bind) == False or self.checkDatePass(bind) == None) and (
                self.checkDatePass(quand) == False or self.checkDatePass(quand) == None)):
            self.server.set_name(name)
            self.server.set_office(office)
            self.server.set_departament(departament)
            self.server.set_reason(reason)
            self.server.set_process(process)
            self.server.set_type_process(self.type_proProfile)
            self.server.set_contact(contact)
            self.server.set_type_number(self.TypeProfile)
            self.server.set_biannually_ld(ajustDate(bild))
            self.server.set_biannually_nd(ajustDate(bind))
            self.server.set_quarterly_ld(ajustDate(quald))
            self.server.set_quarterly_nd(ajustDate(quand))
            self.server.set_delete(1)
            self.server.set_evaluate_date(evaluateDate(self.server))
            updateServer(self.server, self.remarksProfile)
            self.cleanProfile()
            self.server = getServer(self.serverSelected)
            self.etNameProfile.insert(0, self.server.get_name())
            self.etNameProfile['state'] = DISABLED
            self.etOfficeProfile.insert(0, self.server.get_office())
            self.etOfficeProfile['state'] = DISABLED
            self.etDepartamentProfile.insert(0, self.server.get_departament())
            self.etDepartamentProfile['state'] = DISABLED
            self.etReasonProfile.insert(0, self.server.get_reason())
            self.etReasonProfile['bg'] = 'white'
            self.etReasonProfile['state'] = DISABLED
            self.etProcessProfile = MaskedWidget(self.frameNumProcessProfile, 'fixed', mask='99999.999999/9999-99',
                                                 width=50, font=self.fontInputs, disabledforeground='black')
            self.etProcessProfile.grid()
            self.etProcessProfile.insert(0, cleanData(self.server.get_process()))
            self.etProcessProfile['state'] = DISABLED
            self.etContactProfile = MaskedWidget(self.frameContactProfile, 'fixed', mask='(99) 99999-9999', bg=self.bg,
                                                 width=20, font=self.fontInputs, disabledforeground='black')
            self.etContactProfile.grid()
            self.etContactProfile.insert(0, cleanData(self.server.get_contact()))
            self.etContactProfile['state'] = DISABLED
            self.etLd_BiProfile = MaskedWidget(self.frameBiProfile, 'fixed', mask='99/99/9999', width=20,
                                               font=self.fontInputs, disabledforeground='black')
            self.etLd_BiProfile.grid(row=2, sticky=W)
            self.etLd_BiProfile.insert(0, reajustDate(cleanData(self.server.get_biannually_ld())))
            self.etLd_BiProfile['state'] = DISABLED
            self.etNd_BiProfile = MaskedWidget(self.frameBiProfile, 'fixed', mask='99/99/9999', width=20,
                                               font=self.fontInputs, disabledforeground='black')
            self.etNd_BiProfile.grid(row=4, sticky=W)
            self.etNd_BiProfile.insert(0, reajustDate(cleanData(self.server.get_biannually_nd())))
            self.etNd_BiProfile['state'] = DISABLED
            self.etLd_QuaProfile = MaskedWidget(self.frameQuaProfile, 'fixed', mask='99/99/9999', width=20,
                                                font=self.fontInputs, disabledforeground='black')
            self.etLd_QuaProfile.grid(row=2, sticky=W)
            self.etLd_QuaProfile.insert(0, reajustDate(cleanData(self.server.get_quarterly_ld())))
            self.etLd_QuaProfile['state'] = DISABLED
            self.etNd_QuaProfile = MaskedWidget(self.frameQuaProfile, 'fixed', mask='99/99/9999', width=20,
                                                font=self.fontInputs, disabledforeground='black')
            self.etNd_QuaProfile.grid(row=4, sticky=W)
            self.etNd_QuaProfile.insert(0, reajustDate(cleanData(self.server.get_quarterly_nd())))
            self.etNd_QuaProfile['state'] = DISABLED
            if self.server.get_type_process() == 'Avaliação da Capadidade Laboral':
                self.varAclProfile.set(1)
                self.checkLcaProfile['state'] = DISABLED
                self.checkRaProfile['state'] = DISABLED
                self.checkRProfile['state'] = DISABLED
            elif self.server.get_type_process() == 'Restrição de atividades':
                self.varRaProfile.set(1)
                self.checkLcaProfile['state'] = DISABLED
                self.checkRaProfile['state'] = DISABLED
                self.checkRProfile['state'] = DISABLED
            elif self.server.get_type_process() == 'Readaptação':
                self.varRProfile.set(1)
                self.checkLcaProfile['state'] = DISABLED
                self.checkRaProfile['state'] = DISABLED
                self.checkRProfile['state'] = DISABLED
            self.TypeProfile = self.server.get_type_number()
            if self.server.get_type_number() == 1:
                self.varUfmaProfile.set(1)
                self.btHuProfile['state'] = DISABLED
                self.btUfmaProfile['state'] = DISABLED
            elif self.server.get_type_number() == 0:
                self.varHuProfile.set(1)
                self.btHuProfile['state'] = DISABLED
                self.btUfmaProfile['state'] = DISABLED
            self.remarksProfile = getRemark(self.server.get_id())
            self.loadTreeRemarkProfile()
            self.frameButtonsProfile.grid(row=1, column=3, padx=90)
            self.frameButtonsEditing.grid_forget()
            self.frameInsertRemarkProfile.grid_forget()
            self.messageInsert = messagebox.showinfo('', 'Atualização concluída!')
        else:
            message = messagebox.showinfo('Atenção',
                                          'As últimas datas de avaliações devem ser anteriores ao dia de hoje e as próximas devem ser posteriores.')

    def on_mainTree_select1(self, event):
        for item in self.treeServers.selection():
            item_text = self.treeServers.item(item, 'values')
            self.serverSelected = item_text[-1]

    def on_mainTree_select2(self, event):
        for item in self.treeServers.selection():
            item_text = self.treeServers.item(item, 'values')
            self.serverSelected = item_text[-1]
            self.mainToProfile()

    def on_mainTreeRemark_select1Profile(self, event):
        for item in self.treeRemarkProfile.selection():
            item_text = self.treeRemarkProfile.index(item)
            self.remarkSelectedProfile = int(item_text)

    def on_mainTreeRemark_select2Profile(self, event):
        for item in self.treeRemarkProfile.selection():
            item_text = self.treeRemarkProfile.index(item)
            self.remarkSelectedProfile = int(item_text)
            self.viewRemarkProfile()

    def on_mainTreeRemark_select1(self, event):
        for item in self.treeRemark.selection():
            item_text = self.treeRemark.index(item)
            self.remarkSelected = int(item_text)

    def on_mainTreeRemark_select2(self, event):
        for item in self.treeRemark.selection():
            item_text = self.treeRemark.index(item)
            self.remarkSelected = int(item_text)
            self.viewRemark()

    def mainToEdit(self):
        if self.serverSelected != None:
            self.frameMain.pack_forget()
            self.Profile.pack(side=TOP, anchor=W, padx=70)
            self.server = getServer(self.serverSelected)
            self.server.set_id(self.serverSelected)
            self.etNameProfile.insert(0, self.server.get_name())
            self.etOfficeProfile.insert(0, self.server.get_office())
            self.etDepartamentProfile.insert(0, self.server.get_departament())
            self.etReasonProfile.insert(0, self.server.get_reason())
            self.etProcessProfile = MaskedWidget(self.frameNumProcessProfile, 'fixed', mask='99999.999999/9999-99',
                                                 width=50, font=self.fontInputs, disabledforeground='black')
            self.etProcessProfile.grid()
            self.etProcessProfile.insert(0, cleanData(self.server.get_process()))
            self.etContactProfile = MaskedWidget(self.frameContactProfile, 'fixed', mask='(99) 99999-9999', bg=self.bg,
                                                 width=20, font=self.fontInputs, disabledforeground='black')
            self.etContactProfile.grid()
            self.etContactProfile.insert(0, cleanData(self.server.get_contact()))
            self.etLd_BiProfile = MaskedWidget(self.frameBiProfile, 'fixed', mask='99/99/9999', width=20,
                                               font=self.fontInputs,
                                               disabledforeground='black')
            self.etLd_BiProfile.grid(row=2, sticky=W)
            self.etLd_BiProfile.insert(0, reajustDate(cleanData(self.server.get_biannually_ld())))
            self.etNd_BiProfile = MaskedWidget(self.frameBiProfile, 'fixed', mask='99/99/9999', width=20,
                                               font=self.fontInputs,
                                               disabledforeground='black')
            self.etNd_BiProfile.grid(row=4, sticky=W)
            self.etNd_BiProfile.insert(0, reajustDate(cleanData(self.server.get_biannually_nd())))
            self.etLd_QuaProfile = MaskedWidget(self.frameQuaProfile, 'fixed', mask='99/99/9999', width=20,
                                                font=self.fontInputs,
                                                disabledforeground='black')
            self.etLd_QuaProfile.grid(row=2, sticky=W)
            self.etLd_QuaProfile.insert(0, reajustDate(cleanData(self.server.get_quarterly_ld())))
            self.etNd_QuaProfile = MaskedWidget(self.frameQuaProfile, 'fixed', mask='99/99/9999', width=20,
                                                font=self.fontInputs,
                                                disabledforeground='black')
            self.etNd_QuaProfile.grid(row=4, sticky=W)
            self.etNd_QuaProfile.insert(0, reajustDate(cleanData(self.server.get_quarterly_nd())))
            self.type_proProfile = self.server.get_type_process()
            if self.server.get_type_process() == 'Avaliação da Capacidade Laboral':
                self.varAclProfile.set(1)
            elif self.server.get_type_process() == 'Restrição de atividades':
                self.varRaProfile.set(1)
            elif self.server.get_type_process() == 'Readaptação':
                self.varRProfile.set(1)
            self.TypeProfile = self.server.get_type_number()
            if self.server.get_type_number() == 1:
                self.varUfmaProfile.set(1)
            elif self.server.get_type_number() == 0:
                self.varHuProfile.set(1)
            self.remarksProfile = getRemark(self.server.get_id())
            for item in self.remarksProfile:
                self.treeRemarkProfile.insert('', 'end', values=item)
            self.frameButtonsProfile.grid_forget()
            self.frameButtonsEditing.grid(row=1, column=3, padx=90)
            self.frameInsertRemarkProfile.grid(row=0, column=3, padx=50)
        else:
            self.messageInsert = messagebox.showinfo('', 'Selecione um servidor!')

    def excludeServer(self):
        if self.serverSelected != None:
            self.server = getServer(self.serverSelected)
            self.server.set_id(self.serverSelected)
            excludeServers(self.server)
            self.server = None
            self.loadServersTree(self.varClassific)
            self.messageInsert = messagebox.showinfo('', 'Servidor excluído com sucesso!')
        else:
            self.messageInsert = messagebox.showinfo('', 'Selecione um servidor!')

    def excludeServerProfile(self):
        self.loadServersTree(self.varClassific)
        self.frameMain.pack(fill='both', expand=True)
        self.Profile.pack_forget()
        self.type_pro, self.Type = None, None
        self.etNameProfile['state'] = NORMAL
        self.etOfficeProfile['state'] = NORMAL
        self.etDepartamentProfile['state'] = NORMAL
        self.etReasonProfile['state'] = NORMAL
        self.checkLcaProfile['state'] = NORMAL
        self.checkRaProfile['state'] = NORMAL
        self.checkRProfile['state'] = NORMAL
        self.btUfmaProfile['state'] = NORMAL
        self.btHuProfile['state'] = NORMAL
        self.etNameProfile.delete(0, END)
        self.etOfficeProfile.delete(0, END)
        self.etProcessProfile.destroy()
        self.etContactProfile.destroy()
        self.etReasonProfile.delete(0, END)
        self.etDepartamentProfile.delete(0, END)
        self.etLd_QuaProfile.destroy()
        self.etLd_BiProfile.destroy()
        self.etNd_BiProfile.destroy()
        self.etNd_QuaProfile.destroy()
        self.varUfmaProfile.set(0)
        self.varHuProfile.set(0)
        self.varRaProfile.set(0)
        self.varRProfile.set(0)
        self.varAclProfile.set(0)
        self.treeRemarkProfile.delete(*self.treeRemarkProfile.get_children())
        excludeServers(self.server)
        self.server = None
        self.remarksProfile = []
        self.messageInsert = messagebox.showinfo('', 'Servidor excluído com sucesso!')

    def search(self):
        self.varClassific = 2
        self.varClassificHu.set(0)
        self.varClassificUfma.set(0)
        self.varClassificAll.set(0)
        search = self.etSearch.get()
        search = search.lower()
        self.treeServers.delete(*self.treeServers.get_children())
        tree_data = getSearchDataServers(search)
        if len(tree_data) == 0:
            messageSearchErro = messagebox.showwarning('', 'Nenhum servidor encontrado!')
            self.varClassific = None
            self.loadServersTree(self.varClassific)
        else:
            for item in tree_data:
                self.treeServers.insert('', 'end', values=item[:6])

    def sortby(self, tree, col, descending):
        """Sort tree contents when a column is clicked on."""
        # grab values to sort
        data = [(tree.set(child, col), child) for child in tree.get_children('')]

        # reorder data
        data.sort(reverse=descending)
        for indx, item in enumerate(data):
            tree.move(item[1], '', indx)

    def checkDatePass(self, date):
        if date != '__/__/____':
            if datetime.strptime(date, '%d/%m/%Y') > datetime.now():
                return False
            elif datetime.strptime(date, '%d/%m/%Y') < datetime.now():
                return True
            else:
                return None


Root = Tk()
Root.title('Projeto Readaptar')
RootScreen = Main(Root)
Root.mainloop()
