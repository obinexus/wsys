# =============================================================================
# Makefile: PLP-128 Sparse Coordinate Functor
# Author: obinexus (first-person: I built this so I can think in polar or cartesian)
# Third-person: obinexus built this so *anyone* can think in polar or cartesian
#
# GOAL: One command → everything works on Linux & macOS
# COMMANDS:
#   make all      → build everything
#   make build    → compile C → .so
#   make run      → run Python demo
#   make demo     → compile & run C example
#   make clean    → remove build artifacts
#
# ISOMORPHIC: This Makefile *mirrors* README.md — same commands, same flow
# =============================================================================

# === CONFIGURATION ===========================================================
CC      := gcc
CFLAGS  := -Wall -Wextra -O2 -fPIC
LDFLAGS := -shared
LDLIBS  := -lm

# Detect OS
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    SO_EXT   := dylib
    SO_FLAGS := -dynamiclib
else
    SO_EXT   := so
    SO_FLAGS := $(LDFLAGS)
endif

# === PATHS (isomorphic to repo) ==============================================
SRC_DIR     := sparse_coord/src
LIB_DIR     := sparse_coord/lib
BIN_DIR     := sparse_coord/bin
INC_DIR     := sparse_coord/include
EXAMPLES    := examples
BUILD_DIR   := .build

# === FILES ===================================================================
PLP_SRC     := $(SRC_DIR)/plp128.c
PLP_HDR     := $(INC_DIR)/plp128.h
PLP_SO      := $(LIB_DIR)/plp128.$(SO_EXT)

SPARSE_SRC  := $(SRC_DIR)/sparse_coord.c
SPARSE_SO   := $(LIB_DIR)/libsparse_coord.$(SO_EXT)

DEMO_SRC    := $(EXAMPLES)/demo_cart2pol.c
DEMO_BIN    := $(BUILD_DIR)/demo_cart2pol

PYTHON_DEMO := sparse_coord/main.py

# === DEFAULT TARGET ==========================================================
.PHONY: all
all: build run demo

# === BUILD C LIBRARIES =======================================================
$(LIB_DIR):
    @echo "Creating lib directory..."
    @mkdir -p $@

$(BUILD_DIR):
    @mkdir -p $@

# PLP-128 Shared Library
$(PLP_SO): $(PLP_SRC) $(PLP_HDR) | $(LIB_DIR)
    @echo "Building PLP-128 shared library... ($(SO_EXT))"
    @$(CC) $(CFLAGS) $(SO_FLAGS) $< $(LDLIBS) -o $@

# Sparse Coord (legacy) – optional
$(SPARSE_SO): $(SPARSE_SRC) | $(LIB_DIR)
    @echo "Building legacy sparse_coord.so..."
    @$(CC) $(CFLAGS) $(SO_FLAGS) $< $(LDLIBS) -o $@

# === BUILD DEMO ==============================================================
$(DEMO_BIN): $(DEMO_SRC) $(PLP_SO) | $(BUILD_DIR)
    @echo "Compiling C demo..."
    @$(CC) $(CFLAGS) $< -I$(INC_DIR) -L$(LIB_DIR) -lplp128 $(LDLIBS) -o $@

# === PHONY TARGETS ===========================================================
.PHONY: build compile
build compile: $(PLP_SO) $(SPARSE_SO)
    @echo "Build complete. Libraries in: $(LIB_DIR)"

.PHONY: run
run: $(PLP_SO)
    @echo "Running Python demo..."
    @python3 $(PYTHON_DEMO) cart 12 5
    @python3 $(PYTHON_DEMO) pol 13 22.62

.PHONY: demo
demo: $(DEMO_BIN)
    @echo "Running C demo..."
    @LD_LIBRARY_PATH=$(LIB_DIR):$$LD_LIBRARY_PATH DYLD_LIBRARY_PATH=$(LIB_DIR):$$DYLD_LIBRARY_PATH $<

.PHONY: clean
clean:
    @echo "Cleaning build artifacts..."
    @rm -rf $(BUILD_DIR) $(LIB_DIR)/*.$(SO_EXT) $(LIB_DIR)/*.dylib
    @echo "Clean complete."

.PHONY: help
help:
    @echo "Available targets:"
    @echo "  make all     → build + run + demo"
    @echo "  make build   → compile C → .so/.dylib"
    @echo "  make run     → run Python demo"
    @echo "  make demo    → compile & run C example"
    @echo "  make clean   → remove build files"
    @echo "  make help    → show this message"

# === DEFAULT =================================================================
.DEFAULT_GOAL := help
