VENV   := .venv
PYTHON := $(VENV)/bin/python3
PIP    := $(VENV)/bin/pip

# ─────────────────────────────────────────────────────────────
# Clean previous builds (editable & wheels)
# ─────────────────────────────────────────────────────────────
CLEAN_SKBUILD := rm -rf skbuild-editable dist

# ─────────────────────────────────────────────────────────────
# Helper for green echo
# ─────────────────────────────────────────────────────────────
define echo_green
	@echo "\033[0;32m$(1)\033[0m"
endef

# ─────────────────────────────────────────────────────────────
# Virtual-env bootstrap
# ─────────────────────────────────────────────────────────────
$(VENV)/bin/activate:
	$(call echo_green, "🐍 Setting up virtual environment…")
	python3 -m venv $(VENV)
	$(call echo_green, "📦 Installing base Python dependencies…")
	$(PIP) install --upgrade pip
	$(PIP) install clang-format faker      # global dev tools

# ─────────────────────────────────────────────────────────────
# Clang-format helpers
# ─────────────────────────────────────────────────────────────
IMAGE := ghcr.io/azimafroozeh/clang-format-python/clang-format-python:14

format:
	$(call echo_green,"Formatting…")
	docker run --rm -v "$$(pwd)":/app -w /app $(IMAGE) \
	    bash -c "python3 scripts/run-clang-format.py -r examples include src benchmark python test data/include -i --exclude include/fls/json/nlohmann"

clang-format:
	$(call echo_green, "Running clang-format with Docker…")
	docker run --rm -v "$$(pwd)":/app -w /app ubuntu:22.04 \
	    bash -c "apt update && apt install -y python3 clang-format-14 && ln -s /usr/bin/clang-format-14 /usr/bin/clang-format && \
	             python3 scripts/run-clang-format.py -r examples include src benchmark test data/include python -i --exclude include/fls/json/nlohmann"

format-check:
	$(call echo_green, "Checking formatting…")
	docker run --rm -v "$$(pwd)":/app -w /app ubuntu:22.04 \
	    bash -c "apt update && apt install -y clang-format-14 python3 && ln -s /usr/bin/clang-format-14 /usr/bin/clang-format && \
	             python3 scripts/run-clang-format.py -r examples include src benchmark test data/include python --exclude include/fls/json/nlohmann"

# ─────────────────────────────────────────────────────────────
# Data & history helpers
# ─────────────────────────────────────────────────────────────
generate_syntethic_data: $(VENV)/bin/activate
	$(call echo_green, "Generating synthetic data…")
	cd scripts && PYTHONPATH=$(PWD) ../$(PYTHON) generate_synthetic_data.py

check_fastlanes_result_history: $(VENV)/bin/activate
	$(call echo_green, "Checking CSV history…")
	cd scripts && ../$(PYTHON) check_fastlanes_result_history.py

time_ctest:
	$(call echo_green, "Running ctest with timing…")
	cd cmake-build-release && time ctest --output-on-failure

# ─────────────────────────────────────────────────────────────
# Python bindings
# ─────────────────────────────────────────────────────────────
PY_DEPS := \
  scikit-build-core>=0.7,<0.8 \
  pybind11>=2.12,<2.13 \
  setuptools_scm[toml]>=7,<8 \
  pytest \
  ninja>=1.5 \
  pyproject_metadata

TEST_DIR := python/tests

.PHONY: check_python_deps rebuild_python_debug rebuild_python_release clean_python \
        run_example_python test_python build_wheel_release upload_pypi upload_testpypi

check_python_deps: $(VENV)/bin/activate
	$(call echo_green, "📦 Ensuring Python build deps…")
	$(PIP) install --upgrade $(patsubst %,"%",$(PY_DEPS))

rebuild_python_debug: $(VENV)/bin/activate
	@echo "🔄 Rebuilding PyFastLanes bindings (Debug)…"
	$(CLEAN_SKBUILD)
	CMAKE_BUILD_TYPE=Debug \
	CMAKE_BUILD_PARALLEL_LEVEL=12 \
	CMAKE_VERBOSE_MAKEFILE=ON \
	PIP_VERBOSE=1 \
	$(PYTHON) -m pip install -e . --no-build-isolation -v

rebuild_python_release: $(VENV)/bin/activate
	@echo "🚀 Rebuilding PyFastLanes bindings (Release)…"
	$(CLEAN_SKBUILD)
	CMAKE_BUILD_TYPE=Release \
	CMAKE_BUILD_PARALLEL_LEVEL=12 \
	CMAKE_VERBOSE_MAKEFILE=ON \
	PIP_VERBOSE=1 \
	$(PYTHON) -m pip install -e . --no-build-isolation -v

clean_python:
	$(call echo_green,"🧹 Cleaning Python artefacts…")
	rm -rf skbuild-editable dist
	find python/pyfastlanes -name '_pyfastlanes*.so' -delete
	find . -name '__pycache__'   -exec rm -rf {} +
	find . -name '*.pyc'         -delete

run_example_python: $(VENV)/bin/activate
	$(call echo_green,"🚀 Running example…")
	$(PYTHON) examples/python_example.py

test_python: rebuild_python_release
	$(call echo_green, "🧪 Running unit tests…")
	PYTHONPATH=$(PWD)/python $(PYTHON) -m pytest -q $(TEST_DIR)

# ─────────────────────────────────────────────────────────────
# Wheel build & upload
# ─────────────────────────────────────────────────────────────
build_wheel_release: $(VENV)/bin/activate
	@echo "📦 Building PyFastLanes wheel (Release)…"
	$(PIP) install --upgrade $(patsubst %,"%",$(PY_DEPS))
	$(CLEAN_SKBUILD)
	CMAKE_BUILD_TYPE=Release \
	CMAKE_BUILD_PARALLEL_LEVEL=12 \
	CMAKE_VERBOSE_MAKEFILE=ON \
	PIP_VERBOSE=1 \
	$(PYTHON) -m build --wheel --no-isolation --outdir dist

upload_pypi: $(VENV)/bin/activate
	$(call echo_green, "🚀 Uploading to PyPI…")
	$(PYTHON) -m twine upload dist/*

upload_testpypi: $(VENV)/bin/activate
	$(call echo_green, "🧪 Uploading to TestPyPI…")
	$(PYTHON) -m twine upload --repository testpypi dist/*

# ─────────────────────────────────────────────────────────────
# Build just the source distribution (fast, setuptools-based)
# ─────────────────────────────────────────────────────────────
build_sdist: $(VENV)/bin/activate
	$(call echo_green, "📦 Building source distribution…")
	# Ensure we have the right versions of setuptools_scm, etc.
	$(PIP) install --upgrade setuptools wheel
	$(PIP) install --upgrade $(patsubst %,"%",$(PY_DEPS))
	# Now build sdist without CMake hangs
	$(PYTHON) -m build --sdist --no-isolation --outdir dist

