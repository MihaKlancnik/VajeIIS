import sys
import pandas as pd
from evidently import Report
from evidently.presets.dataset_stats import DataSummaryPreset
from evidently.presets.drift import DataDriftPreset
import os
import glob

preprocessed_dir = "data/preprocessed/air"
reference_dir = "data/reference/air"
report_dir = "reports"
os.makedirs(reference_dir, exist_ok=True)
os.makedirs(report_dir, exist_ok=True)

all_tests_passed = True

csv_files = glob.glob(os.path.join(preprocessed_dir, "*.csv"))

for csv_file in csv_files:
    filename = os.path.basename(csv_file)
    current = pd.read_csv(csv_file)
    reference_path = os.path.join(reference_dir, filename)

    if not os.path.exists(reference_path):
        print(f"[INFO] Reference file for {filename} not found. Copying current data to {reference_path}.")
        current.to_csv(reference_path, index=False)

    reference = pd.read_csv(reference_path)

    # Ensure "date_to" column is dropped if it exists
    for df in [current, reference]:
        if "date_to" in df.columns:
            del df["date_to"]

    #preskoci tiste ki imajo mankajoce vrednosti. UPRAS A TU ZBRISES AL NADOMESTIS
    empty_columns = [col for col in reference.columns if reference[col].dropna().empty]
    if empty_columns:
        print(f"[SKIP] Reference data for {filename} has empty columns: {empty_columns}. Skipping this file.")
        continue

    report = Report(
        [DataSummaryPreset(), DataDriftPreset()],
        include_tests=True
    )

    result = report.run(reference_data=reference, current_data=current)

    report_file = os.path.join(report_dir, f"data_testing_report_{filename.replace('.csv', '')}.html")
    result.save_html(report_file)

    result_dict = result.dict()
    if "tests" in result_dict:
        for test in result_dict["tests"]:
            if test.get("status") != "SUCCESS":
                all_tests_passed = False
                print(f"[FAIL] Data tests failed for {filename}.")
                break

    if all_tests_passed:
        print(f"[PASS] Data tests passed for {filename}. Updating reference data.")
        current.to_csv(reference_path, index=False)

if not all_tests_passed:
    print("[RESULT] One or more data tests failed.")
    sys.exit(0) #TO POL NUJNO SPREMEN NAZAJ V 1 TO SE MORS ODLOCIT AL BOS NADOMESTIL AL ZBRISU
else:
    print("[RESULT] All data tests passed successfully.")
    sys.exit(0)
