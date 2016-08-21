########################################################################
#   __                                                                 #
#  |  |            __      __    __   __    __    ______    __    _    #
#  |  |           /  \    |  |  |  | |  \  |  |  /  __  \  |  |  |  |  #
#  |  |          / /\ \   |  |  |  | |   \ |  | |  /  \__| |  |__|  |  #
#  |  |         /  __  \  |  |__|  | |    \|  | | |    __  |   __   |  #
#  |  |_____   /  /  \  \ |        | |  |\    | |  \__/  | |  |  |  |  #
#  |________| /__/    \__\ \______/  |__| \___|  \______/  |__|  |__|  #
#               __                                                     #
#              |  |         __    __    __    __   ___                 #
#              |  |        |  |  |  \  |  |  |  | /  /                 #
#              |  |        |  |  |   \ |  |  |  |/  /                  #
#              |  |        |  |  |    \|  |  |      \                  #
#              |  |_____   |  |  |  |\    |  |  |\   \                 #
#              |________|  |__|  |__| \___|  |__| \___\                #
#                                                                      #
########################################################################


import sys
import gl2
import LL_resources

try:
    from PyQt4 import QtCore, QtGui
except ImportError:
    print "\nPyQt4 is required to run LaunchLink. Please see readme.txt\n"
    a = raw_input("Press Enter")
    sys.exit()

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


def get_timezone():
    t_zones = ["UTC-5   EST", "UTC-6   AST", "UTC-7   MST", "UTC-8   PST",
               "UTC+0  GMT", "UTC+1  CET", "UTC+2", "UTC+3", "UTC+4",
               "UTC+5", "UTC+6", "UTC+7", "UTC+8", "UTC+9", "UTC+10",
               "UTC+11", "UTC+12", "UTC+13"]
    title = "Time Zone"
    msg = "Select time zone:"
    item, ok = QtGui.QInputDialog.getItem(None, title, msg, t_zones, 0, False)
    if ok and item:
        if item == "UTC-5   EST":
            timezone = "EST"
        elif item == "UTC-6   AST":
            timezone = "AST"
        elif item == "UTC-7   MST":
            timezone = "MST"
        elif item == "UTC-8   PST":
            timezone = "PST"
        elif item == "UTC+0  GMT":
            timezone = "GMT"
        elif item == "UTC+1  CET":
            timezone = "CET"
        else:
            timezone = str(item)
        return timezone
    else:
        sys.exit()


# ______________________________________________________________________
# ======================================================================


class LaunchLinkUi(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

    # Use dialog box to get timezone from user
        self.timezone = get_timezone()

    # Variable declarations
        self.d = None
        self.number_of_launches = None
        self.tbd = None
        self.launch_date = None
        self.launch_date_conv = None
        self.stream_link = None
        self.map_link = None
        self.temp_cd = None
        self.notified_1day = 0
        self.notified_1hour = 0

        red = "color: rgb(210, 90, 50);"
        white = "color: rgb(200,200,200);"
        dark_grey = "color: rgb(38, 38, 38);"
        grey = "color: rgb(75,75,75);"
        self.grey = grey
        font10 = "font: 10pt Arial;"
        font12 = "font: 12pt Arial;"
        font14 = "font: 14pt Arial;"
        self.font14 = font14
        font16 = "font: 16pt Arial;"
        font18 = "font: 18pt Arial;"
        grey_bg = "background-color: rgb(38, 38, 38);"
        med_grey = "background-color: rgb(75, 75, 75);"
        self.med_grey = med_grey
        light_bg = "background-color: rgb(105, 105, 105);"
        self.light_bg = light_bg
        alt_shade_rows = "background-color: rgb(105, 105, 105); alternate-background-color: \
                          rgb(85,85,85); selection-color: rgb(200, 200, 200);"

    # Widget main window
        self.resize(900, 700)
        self.setStyleSheet(grey_bg + white + "selection-background-color: rgb(50,50,200);")

    # Icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/LL_icon2a.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.horizontalLayout_2 = QtGui.QHBoxLayout(self)

        self.frame_left = QtGui.QFrame(self)

        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame_left)

    # Upcoming launches label
        self.label_launch = QtGui.QLabel(self.frame_left)
        self.label_launch.setStyleSheet(font14)
        self.verticalLayout_3.addWidget(self.label_launch)

    # Launch list
        self.listWidget = QtGui.QListWidget(self.frame_left)
        self.listWidget.setWordWrap(True)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setStyleSheet(alt_shade_rows + font12 + dark_grey)
        self.verticalLayout_3.addWidget(self.listWidget)

        self.horizontalLayout_2.addWidget(self.frame_left)

        self.frame_right = QtGui.QFrame(self)

        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(1)
        self.frame_right.setSizePolicy(size_policy)

        self.verticalLayout_4 = QtGui.QVBoxLayout(self.frame_right)

    # Static launch info labels
        self.label_launch_name = QtGui.QLabel(self.frame_right)
        self.label_launch_name.setStyleSheet(font16)
        self.label_launch_name.setWordWrap(True)
        self.label_launch_name.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_4.addWidget(self.label_launch_name)

        self.label_launch_countdown = QtGui.QLabel(self.frame_right)
        self.label_launch_countdown.setStyleSheet(font18 + red)
        self.label_launch_countdown.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_4.addWidget(self.label_launch_countdown)

        self.label_launch_date = QtGui.QLabel(self.frame_right)
        self.label_launch_date.setStyleSheet(font14)
        self.label_launch_date.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_4.addWidget(self.label_launch_date)

        self.label_launch_location = QtGui.QLabel(self.frame_right)
        self.label_launch_location.setStyleSheet(font14)
        self.label_launch_location.setWordWrap(True)
        self.label_launch_location.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_4.addWidget(self.label_launch_location)

    # Tab widget
        self.tabWidget = QtGui.QTabWidget(self.frame_right)
        self.tabWidget.setStyleSheet(font10)

    # Launch tab -------------------------------------------------------
        self.tab_launch = QtGui.QWidget()
        self.tab_launch.setStyleSheet(med_grey)
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab_launch)

        self.scrollArea_launch = QtGui.QScrollArea(self.tab_launch)
        self.scrollArea_launch.setWidgetResizable(True)
        self.scrollArea_launch.setStyleSheet(light_bg)
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 451, 446))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)

        self.label_list_launch = list(xrange(18))
        for i in range(0, 12, 2):
            self.label_list_launch[i] = QtGui.QLabel(self.scrollAreaWidgetContents)
            self.label_list_launch[i].setWordWrap(True)
            self.verticalLayout_8.addWidget(self.label_list_launch[i])
            self.label_list_launch[i].setStyleSheet(font12 + dark_grey)

            self.label_list_launch[i+1] = QtGui.QLabel(self.scrollAreaWidgetContents)
            self.label_list_launch[i+1].setIndent(20)
            self.label_list_launch[i+1].setOpenExternalLinks(True)
            self.verticalLayout_8.addWidget(self.label_list_launch[i+1])
            self.label_list_launch[i+1].setStyleSheet(font12)
            self.label_list_launch[i+1].setWordWrap(True)

        spacer_item = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacer_item)
        self.scrollArea_launch.setWidget(self.scrollAreaWidgetContents)

        self.scrollArea_launch.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_5.addWidget(self.scrollArea_launch)
        self.tabWidget.addTab(self.tab_launch, "Launch")

    # Mission Tab ------------------------------------------------------
        self.tab_mission = QtGui.QWidget()
        self.tab_mission.setStyleSheet(med_grey)
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.tab_mission)

        self.scrollArea_mission = QtGui.QScrollArea(self.tab_mission)
        self.scrollArea_mission.setWidgetResizable(True)
        self.scrollArea_mission.setStyleSheet(light_bg)
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 451, 446))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents_2)

        self.label_list_mission = list(xrange(10))
        for i in range(0, 8, 2):
            self.label_list_mission[i] = QtGui.QLabel(self.scrollAreaWidgetContents)
            self.label_list_mission[i].setWordWrap(True)
            self.verticalLayout_9.addWidget(self.label_list_mission[i])
            self.label_list_mission[i].setStyleSheet(font12 + dark_grey)

            self.label_list_mission[i+1] = QtGui.QLabel(self.scrollAreaWidgetContents)
            self.label_list_mission[i+1].setIndent(20)
            self.label_list_mission[i+1].setOpenExternalLinks(True)
            self.verticalLayout_9.addWidget(self.label_list_mission[i+1])
            self.label_list_mission[i+1].setStyleSheet(font12)
            self.label_list_mission[i+1].setWordWrap(True)

        spacer_item = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacer_item)
        self.scrollArea_launch.setWidget(self.scrollAreaWidgetContents)

        self.scrollArea_mission.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_6.addWidget(self.scrollArea_mission)
        self.tabWidget.addTab(self.tab_mission, "Mission")

    # Rocket tab -------------------------------------------------------
        self.tab_rocket = QtGui.QWidget()
        self.tab_rocket.setStyleSheet(med_grey)
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.tab_rocket)

        self.scrollArea_rocket = QtGui.QScrollArea(self.tab_rocket)
        self.scrollArea_rocket.setWidgetResizable(True)
        self.scrollArea_rocket.setStyleSheet(light_bg)
        self.scrollAreaWidgetContents_3 = QtGui.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 451, 446))
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents_3)

        self.label_list_rocket = list(xrange(12))
        for i in range(0, 10, 2):
            self.label_list_rocket[i] = QtGui.QLabel(self.scrollAreaWidgetContents)
            self.label_list_rocket[i].setWordWrap(True)
            self.verticalLayout_10.addWidget(self.label_list_rocket[i])
            self.label_list_rocket[i].setStyleSheet(font12 + dark_grey)

            self.label_list_rocket[i+1] = QtGui.QLabel(self.scrollAreaWidgetContents)
            self.label_list_rocket[i+1].setIndent(20)
            self.label_list_rocket[i+1].setOpenExternalLinks(True)
            self.verticalLayout_10.addWidget(self.label_list_rocket[i+1])
            self.label_list_rocket[i+1].setStyleSheet(font12)
            self.label_list_rocket[i+1].setWordWrap(True)

        spacer_item = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacer_item)
        self.scrollArea_launch.setWidget(self.scrollAreaWidgetContents)

        self.scrollArea_rocket.setWidget(self.scrollAreaWidgetContents_3)
        self.verticalLayout_7.addWidget(self.scrollArea_rocket)
        self.tabWidget.addTab(self.tab_rocket, "Rocket")

        self.verticalLayout_4.addWidget(self.tabWidget)

        self.horizontalLayout_3 = QtGui.QHBoxLayout()

        self.tabWidget.setCurrentIndex(0)

    # Stream button
        self.button_stream = QtGui.QPushButton()
        self.button_stream.setStyleSheet(font14 + med_grey)
        self.horizontalLayout_3.addWidget(self.button_stream)

    # Map button
        self.button_map = QtGui.QPushButton()
        self.button_map.setStyleSheet(font14 + med_grey)
        self.horizontalLayout_3.addWidget(self.button_map)

        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2.addWidget(self.frame_right)

    # Splitter
        self.splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.splitter1.addWidget(self.frame_left)

        self.splitter2 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.splitter2.addWidget(self.splitter1)
        self.splitter2.addWidget(self.frame_right)

        self.horizontalLayout_2.addWidget(self.splitter2)

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Plastique'))

    # Signals & Slots
        self.listWidget.currentItemChanged.connect(self.update_ui)
        self.button_map.clicked.connect(self.map_button)
        self.button_stream.clicked.connect(self.stream_button)
        QtCore.QMetaObject.connectSlotsByName(self)

    # Static label text
        self.setWindowTitle("LaunchLink")
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.label_launch.setText("Upcoming Launches:")
        self.button_map.setText("Map")
        self.button_stream.setText("Stream")

    # Get info and populate UI
        self.refresh_dict()
        self.listWidget.setCurrentRow(0)

    # Countdown timer (create, connect, start)
        self.cd_timer = QtCore.QTimer()
        self.cd_timer.timeout.connect(self.update_countdown)
        self.cd_timer.start(100)

    # Refresh timer (create, connect, start) - refreshes every 2 hours
        self.refresh_timer = QtCore.QTimer()
        self.refresh_timer.timeout.connect(self.refresh_dict)
        self.refresh_timer.start(7200000)   # 1000 * 60 * 60 * 2

    # UI FUNCTIONS =====================================================

    def refresh_dict(self):
        # Refreshes info and repopulates UI
        # Displays splash screen overlay while processing
        splash_pix = QtGui.QPixmap(':/img/LaunchLink_Logo_SM2.png')
        splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())
        splash.show()
        app.processEvents()
        self.d = gl2.get_launches(25)
        self.fill_launch_list()
        self.update_ui()
        splash.finish(self)

    def fill_launch_list(self):
        # Clears and refreshes launch list
        # Returns to previously selected list item after refresh
        current = self.listWidget.currentRow()
        self.listWidget.clear()
        self.number_of_launches = len(self.d['launches'])
        for i in xrange(self.number_of_launches):
            item = QtGui.QListWidgetItem()
            self.listWidget.addItem(item)
            item = self.listWidget.item(i)
            text = _fromUtf8(self.d['launches'][i]['name'])
            item.setText(text)
        self.listWidget.setCurrentRow(current)

    def fill_launch_information(self, sel=0):
        # Processes and populates information for selected launch
        launch_name = "<b>" + _fromUtf8(self.d['launches'][sel]['name'] + "</b>")
        self.tbd = self.d['launches'][sel]['tbdtime']
        launch_countdown = gl2.get_countdown(self.d['launches'][sel]['net'])
        self.launch_date = self.d['launches'][sel]['net']
        self.launch_date_conv = gl2.convert_from_utc(self.launch_date, zone=self.timezone)
        if self.tbd == 1:
            launch_countdown = "TBD"
            date_conv = gl2.datetime.strptime(self.launch_date, "%B %d, %Y %H:%M:%S UTC")
            tbd_launch_date = gl2.datetime.strftime(date_conv, "%B %d, %Y")
            self.label_launch_date.setText(tbd_launch_date)
        else:
            self.label_launch_date.setText(self.launch_date_conv)
        launch_location = self.d["launches"][sel]["location"]["pads"][0]["name"]
        self.label_launch_name.setText(launch_name)
        launch_cd = "<b>" + launch_countdown + "</b>"
        self.label_launch_countdown.setText(launch_cd)
        self.label_launch_location.setText(launch_location)

        # Launch tab information ---------------------------------------
        launch_header_list = ("Status:", "Location:", "NET:", "Window Open:", "Window Close:",
                              "Agencies:")
        if self.d['launches'][sel]['location']['pads'][0]['agencies']:
            number_of_launch_agencies = len(self.d['launches'][sel]['location']['pads'][0]['agencies'])
        else:
            number_of_launch_agencies = 0
        launch_agency_list = []
        for agency in range(number_of_launch_agencies):
            a_name = self.d['launches'][sel]['location']['pads'][0]['agencies'][agency]['name']
            if "http" in self.d['launches'][sel]['location']['pads'][0]['agencies'][agency]['infoURL']:
                link = self.d['launches'][sel]['location']['pads'][0]['agencies'][agency]['infoURL']
                info_url = '<a href=\"%s\"><font color="#3232C8">%s</font></span></a>' % (link, a_name)
                a_links = info_url
            else:
                a_links = a_name
            agency_name = "<html><head/><body>%s</body></html>" % a_links
            launch_agency_list.append(agency_name)
            launch_agency_string = "\n".join(launch_agency_list)
        if number_of_launch_agencies == 0:
            launch_agency_string = "Not Available"
        net = gl2.convert_from_utc(self.d['launches'][sel]['net'], zone=self.timezone)
        w_open = gl2.convert_from_utc(self.d['launches'][sel]['windowstart'], zone=self.timezone)
        w_close = gl2.convert_from_utc(self.d['launches'][sel]['windowend'], zone=self.timezone)
        if self.tbd == 1:
            launch_date = self.launch_date[:-12] + "TBD"
            net = launch_date
            w_open = launch_date
            w_close = launch_date
        launch_info_list = [self.d['launches'][sel]['status'],
                            self.d['launches'][sel]['location']['pads'][0]['name'],
                            net,
                            w_open,
                            w_close,
                            launch_agency_string]
        try:
            if "http" in self.d['launches'][sel]['vidURL']:
                link = self.d['launches'][sel]['vidURL']
                self.stream_link = link
                self.button_stream.setEnabled(True)
                self.button_stream.setStyleSheet(self.font14 + self.med_grey)
            else:
                self.button_stream.setEnabled(False)
                self.button_stream.setStyleSheet(self.font14 + self.light_bg + self.grey)
        except KeyError:
            launch_info_list.append("Not Available")
            self.button_stream.setEnabled(False)
            self.button_stream.setStyleSheet(self.font14 + self.light_bg + self.grey)
        try:
            if "http" in self.d['launches'][sel]["location"]["pads"][0]["mapURL"]:
                if "http" in self.d['launches'][sel]["location"]["pads"][0]["mapURL"]:
                    link = self.d['launches'][sel]["location"]["pads"][0]["mapURL"]
                    self.map_link = link
                    self.button_map.setEnabled(True)
                    self.button_map.setStyleSheet(self.font14 + self.med_grey)
                else:
                    self.button_map.setEnabled(False)
                    self.button_map.setStyleSheet(self.font14 + self.light_bg + self.grey)
            else:
                self.button_map.setEnabled(False)
                self.button_map.setStyleSheet(self.font14 + self.light_bg + self.grey)
        except TypeError:
            launch_info_list.append("Not Available")
            self.button_map.setEnabled(False)
            self.button_map.setStyleSheet(self.font14 + self.light_bg + self.grey)
            self.button_stream.setEnabled(False)
            self.button_stream.setStyleSheet(self.font14 + self.light_bg + self.grey)

        for i in range(0, 12, 2):
            self.label_list_launch[i].setText("<b>" + launch_header_list[i/2] + "</b>")
            self.label_list_launch[i+1].setText(str(launch_info_list[i/2]))

        # Mission tab information --------------------------------------
        mission_header_list = ("Mission Type:", "Description:", "Agencies:", "More Information:")
        try:
            number_of_mission_agencies = len(self.d["launches"][sel]["missions"][0]["details"]["agencies"])
        except (IndexError, KeyError):
            number_of_mission_agencies = 0
        mission_agency_list = []
        mission_agency_string = ""
        for agency in range(number_of_mission_agencies):
            m_name = self.d["launches"][sel]["missions"][0]["details"]["agencies"][agency]['name']
            if "http" in self.d["launches"][sel]["missions"][0]["details"]["agencies"][agency]['infoURL']:
                link = self.d["launches"][sel]["missions"][0]["details"]["agencies"][agency]['infoURL']
                info_url = '<a href=\"%s\"><font color="#3232C8">%s</font></span></a>' % (link, m_name)
                m_links = info_url
            else:
                m_links = m_name
            agency_name = "<html><head/><body>%s</body></html>" % m_links
            mission_agency_list.append(agency_name)
            mission_agency_string = "\n".join(mission_agency_list)
        if number_of_mission_agencies == 0:
            mission_agency_string = "Not Available"
        info_links = "<html><head></head><body>"
        if self.d['launches'][sel]["missions"]:
            if "http" in self.d["launches"][sel]["missions"][0]["details"]["infoURL"]:
                link = self.d["launches"][sel]["missions"][0]["details"]["infoURL"]
                info_url = '<a href=\"%s\"><font color="#3232C8">Website</font></span></a>' % link
                info_links += info_url
            if "http" in self.d["launches"][sel]["missions"][0]["details"]["wikiURL"]:
                link = self.d["launches"][sel]["missions"][0]["details"]["wikiURL"]
                wiki_url = '<a href=\"%s\"><font color="#3232C8">Wikipedia</font></span></a>' % (link)
                if "http" in info_links:
                    info_links += "<br>"
                info_links += wiki_url
            if "http" not in info_links:
                info_links += "Not Available"
            info_links += "</body></html>"
            desc = _fromUtf8(self.d["launches"][sel]["missions"][0]["details"]["description"])
            description = desc.replace("\xe2", "\'")
            mission_info_list = (self.d['launches'][sel]["missions"][0]["details"]["type"],
                                 description,
                                 mission_agency_string,
                                 info_links)
        else:
            mission_info_list = []
            for i in range(5):
                mission_info_list.append("Not Available")
        for i in range(0, 8, 2):
            self.label_list_mission[i].setText("<b>" + mission_header_list[i/2] + "</b>")
            self.label_list_mission[i+1].setText(mission_info_list[i/2])

        # Rocket tab information ---------------------------------------
        rocket_header_list = ("Name:", "Family:", "Configuration:", "Agencies:", "More Information:")
        if self.d["launches"][sel]["rocket"]["agencies"]:
            number_of_rocket_agencies = len(self.d["launches"][sel]["rocket"]["agencies"])
        else:
            number_of_rocket_agencies = 0
        rocket_agency_list = []
        for agency in range(number_of_rocket_agencies):
            r_name = self.d["launches"][sel]["rocket"]["agencies"][agency]["name"]
            if "http" in self.d["launches"][sel]["rocket"]["agencies"][agency]['infoURL']:
                link = self.d["launches"][sel]["rocket"]["agencies"][agency]['infoURL']
                info_url = '<a href=\"%s\"><font color="#3232C8">%s</font></span></a>' % (link, r_name)
                r_links = info_url
            else:
                r_links = r_name
            agency_name = "<html><head/><body>%s</body></html>" % r_links
            rocket_agency_list.append(agency_name)
            rocket_agency_string = "\n".join(rocket_agency_list)
        if number_of_rocket_agencies == 0:
            rocket_agency_string = "Not Available"
        rocket_info_list = [self.d["launches"][sel]["rocket"]["name"],
                            self.d["launches"][sel]["rocket"]["familyname"],
                            self.d["launches"][sel]["rocket"]["configuration"],
                            rocket_agency_string]
        for i in xrange(len(rocket_info_list)):
            if rocket_info_list[i] == "":
                rocket_info_list[i] = "Not Available"
        info_links = "<html><head></head><body>"
        try:
            if "http" in self.d["launches"][sel]["rocket"]["details"]["rockets"][0]["infoURL"]:
                link = self.d["launches"][sel]["rocket"]["details"]["rockets"][0]["infoURL"]
                info_url = '<a href=\"%s\"><font color="#3232C8">Website</font></span></a>' % link
                info_links += info_url
        except KeyError:
            pass
        try:
            if "http" in self.d["launches"][sel]["rocket"]["details"]["rockets"][0]["wikiURL"]:
                link = self.d["launches"][sel]["rocket"]["details"]["rockets"][0]["wikiURL"]
                wiki_url = '<a href=\"%s\"><font color="#3232C8">Wikipedia</font></span></a>' % link
                if "http" in info_links:
                    info_links += "<br>"
                info_links += wiki_url
        except KeyError:
            pass
        if "http" not in info_links:
            info_links += "Not Available"
            info_links += "</body></html>"
        rocket_info_list.append(info_links)
        for i in range(0, 10, 2):
            self.label_list_rocket[i].setText("<b>" + rocket_header_list[i/2] + "</b>")
            self.label_list_rocket[i+1].setText(str(rocket_info_list[i/2]))

    def update_countdown(self):
        # Checks if countdown changed and updates the label if it has
        # Sends info dialog when next launch is happening in 1 day
        # Sends info dialog when next launch is happening in 1 hour
        now = gl2.datetime.now()
        net_est = self.launch_date_conv.rsplit(' ', 1)[0]
        net_est_strp = gl2.datetime.strptime(net_est, "%B %d, %Y %H:%M:%S")
        diff = net_est_strp - now
        if self.tbd == 0:
            if diff.days < 0:
                disp_cd = "<b> Liftoff! </b>"
                self.label_launch_countdown.setText(disp_cd)
            elif self.temp_cd != gl2.get_countdown(self.launch_date):
                self.temp_cd = gl2.get_countdown(self.launch_date)
                disp_cd = "<b>" + self.temp_cd + "</b>"
                self.label_launch_countdown.setText(disp_cd)
        if (diff.days == 0) and (diff.seconds > 3599) and (self.notified_1day == 0):
            title = "LaunchLink"
            msg = "Upcoming launch in under 24 hours                   "
            QtGui.QMessageBox.information(self, title, msg)
            self.notified_1day = 1
        if (diff.days == 0) and (diff.seconds < 3600) and (self.notified_1hour == 0):    # 3600 = 60 * 60
            title = "LaunchLink"
            msg = "Upcoming launch in under 1 hour                     "
            QtGui.QMessageBox.information(self, title, msg)
            self.notified_1hour = 1

    def update_ui(self):
        # Slot for list item selection changed signal
        # Refreshes UI information based on currently selected list item
        current = self.listWidget.currentRow()
        self.fill_launch_information(sel=current)

    def stream_button(self):
        # Slot for stream button press signal
        # Corrects "&amp;" to "&"
        # Opens stream link in default web browser
        link = self.stream_link
        link = link.replace("amp;", "")
        gl2.open_link(link)

    def map_button(self):
        # Slot for map button press signal
        # Corrects "&amp;" to "&"
        # Opens map link in default web browser
        link = self.map_link
        link = link.replace("amp;", "")
        gl2.open_link(link)

    def keyPressEvent(self, e):
        # F5 key refreshes info and UI
        # Esc key closes program
        key = e.key()
        if key == QtCore.Qt.Key_F5:
            self.notified_1day = 0
            self.notified_1hour = 0
            self.refresh_dict()
        elif key == QtCore.Qt.Key_Escape:
            self.close()


# ______________________________________________________________________
# ======================================================================


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ll_main = LaunchLinkUi()
    ll_main.show()
    sys.exit(app.exec_())


# ______________________________________________________________________
# ======================================================================
