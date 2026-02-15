@echo off
echo ==========================================
echo Running Epic 4 Tests (Sequential Execution)
echo ==========================================

echo.
echo [1/4] Running Boundary Value Analysis Tests...
python -m pytest tests/test_bva.py -v
if %errorlevel% neq 0 echo [WARN] BVA tests failed!

echo.
echo [2/4] Running Equivalence Partitioning Tests...
python -m pytest tests/test_equivalence.py -v
if %errorlevel% neq 0 echo [WARN] EP tests failed!

echo.
echo [3/4] Running Statement Coverage Tests...
python -m pytest tests/test_statement.py -v
if %errorlevel% neq 0 echo [WARN] Statement tests failed!

echo.
echo [4/4] Running Branch Coverage Tests...
python -m pytest tests/test_branch.py -v
if %errorlevel% neq 0 echo [WARN] Branch tests failed!

echo.
echo ==========================================
echo All tests executed.
echo ==========================================
pause
