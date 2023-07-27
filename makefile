.PHONY: build
.PHONY: clean
.PHONY: install-deps

PYTHON = python3
PIP = pip3

PIP_OPTIONS = --break-system-packages

RM = rm
RM_OPTIONS = -rf
MKDIR = mkdir
MKDIR_OPTIONS = -p
COPY = cp
COPY_OPTIONS = -r


build: install-deps
	cd scripts && $(PYTHON) helper.py
	$(MKDIR) $(MKDIR_OPTIONS) build/dist
	$(COPY)  $(COPY_OPTIONS) assets/*.encrypted build/resources
	pyinstaller 							\
		--distpath build/dist/ 					\
		--specpath build/ 					\
		-F 							\
		--noconfirm 						\
		-p src/ src/main.py					\
		--add-data "resources/intro.encrypted:." 		\
		--add-data "resources/stars_are_right.encrypted:."	\
		--add-data "resources/luck_of_the_draw.encrypted:."	\
		--add-data "resources/last_message.encrypted:."		\
		--add-data "resources/DELETE_THIS.encrypted:."	

install-deps:
	$(PIP) install $(PIP_OPTIONS) -r requirements.txt

clean:
	$(RM) $(RM_OPTIONS) build



