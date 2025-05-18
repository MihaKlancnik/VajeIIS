import sys
import os
import great_expectations as gx

context = gx.get_context()

datasource_name = "air_quality_v8"
data_asset_name = "air_quality_data_v8"
checkpoint_name = "air_quality_checkpoint_v8"
data_directory = os.path.abspath("../data/preprocessed/air")  # Absolute path for safety

all_success = True

# Ensure checkpoint exists without static batch_request
checkpoint = context.add_or_update_checkpoint(
    name=checkpoint_name
)

for filename in os.listdir(data_directory):
    if filename.endswith(".csv"):
        run_id = f"run_{filename}"

        try:
            checkpoint_result = checkpoint.run(
                run_id=run_id,
                batch_request={
                    "datasource_name": datasource_name,
                    "data_asset_name": data_asset_name,
                    "options": {"path": filename},  # Only filename, since base_directory is set correctly
                },
                expectation_suite_name="air_quality_suite" 
            )

            if checkpoint_result["success"]:
                print(f"Validation passed for {filename}!")
            else:
                print(f"Validation failed for {filename}!")
                all_success = False

        except Exception as e:
            print(f"🚨 Error processing {filename}: {e}")
            all_success = False

# Build data docs after processing all files
context.build_data_docs()

