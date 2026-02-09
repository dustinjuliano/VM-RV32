import subprocess
import os
import sys
import unittest

def run_unit_tests():
  print("--- Running Unit Tests ---")
  loader = unittest.TestLoader()
  # Use absolute path for discovery
  start_dir = os.path.dirname(os.path.abspath(__file__))
  tests_dir = os.path.join(start_dir, 'tests')
  suite = loader.discover(tests_dir, pattern='test_*.py')
  runner = unittest.TextTestRunner(verbosity=1)
  result = runner.run(suite)
  return result.wasSuccessful()

def run_examples():
  print("\n--- Running RISC-V Example Verification ---")
  passed = 0
  failed = 0
  all_passed = True

  # Verify tutorial programs
  tests_to_run = []
  if os.path.exists("tutorial"):
      for f in sorted(os.listdir("tutorial")):
          if f.endswith(".s"):
              tests_to_run.append(os.path.join("tutorial", f))

  for tu_path in tests_to_run:
    tu_name = os.path.basename(tu_path)
    print(f"Running {tu_path}...", end=" ", flush=True)
    res = subprocess.run([sys.executable, "main.py", tu_path], 
                         capture_output=True, text=True)
    if res.returncode == 0:
      print("PASSED")
      passed += 1
    else:
      print(f"FAILED (Return code: {res.returncode})")
      if res.stdout: print(res.stdout)
      if res.stderr: print(res.stderr)
      failed += 1
      all_passed = False

  print(f"\n--- Tutorial Results ---")
  print(f"Passed: {passed}")
  print(f"Failed: {failed}")
  return all_passed

if __name__ == '__main__':
  # Ensure we are in the project root
  project_root = os.path.dirname(os.path.abspath(__file__))
  os.chdir(project_root)
  
  unit_success = run_unit_tests()
  tutorials_success = run_examples()
  
  print(f"\n--- Final Status ---")
  print(f"Unit Tests: {'PASSED' if unit_success else 'FAILED'}")
  print(f"Tutorials:  {'PASSED' if tutorials_success else 'FAILED'}")
  
  if not (unit_success and tutorials_success):
    sys.exit(1)
  sys.exit(0)
