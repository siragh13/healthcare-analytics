# Healthcare Analytics Data Dictionary

## Patients

- patient_id: INTEGER, PRIMARY KEY, NOT NULL. Unique identifier for each patient.
- date_of_birth: TEXT, NOT NULL. Patient's date of birth in YYYY-MM-DD format.
- sex: TEXT, NOT NULL. Patient's recorded sex (Male, Female, or Unknown).
- home_region: TEXT, NOT NULL. Geographic region where the patient lives. 
- created_at: TEXT, NOT NULL. UTC timestamp when the patient record was created, in YYYY-MM-DDTHH:MM:SSZ format.

## Departments

- department_id: INTEGER, PRIMARY KEY, NOT NULL. Unique identifier for each department.
- department_name: TEXT, NOT NULL, UNIQUE. Name of the hospital department.
- service_type: TEXT, NOT NULL. Type of department service: emergency or outpatient.
- active_flag: INTEGER, NOT NULL. Indicates whether the department is active (0 = Inactive, 1 = Active).

## ProviderPositions

- position_id: INTEGER, PRIMARY KEY, NOT NULL. Unique identifier for each authorized provider position. 
- department_id: INTEGER, NOT NULL, FOREIGN KEY. References Departments(department_id). Identifies the department assigned to this position.
- role: TEXT, NOT NULL. Type of healthcare provider assigned to this positon: physician, nurse_practitioner, or physician_assistant.  
- authorized_fte: REAL, NOT NULL. Full-time equivalent allocated to this provider position. Set to 1.0 for every position.
- position_start_date: TEXT, NOT NULL. Date the provider position became active, in YYYY-MM-DD format.
- position_end_date: TEXT, NULL. Date the provider position was permanently closed, in YYYY-MM-DD format. NULL if the position remains active.

## Providers 

- provider_id: INTEGER, PRIMARY KEY, NOT NULL. Unique identifier for each individual provider.
- position_id: INTEGER, NOT NULL, FOREIGN KEY. References ProviderPositions(position_id). Identifies the authorized position assigned to this provider.
- role: TEXT, NOT NULL. Type of healthcare provider: physician, nurse_practitioner, or physician_assistant.  
- employment_start_date: TEXT, NOT NULL. Date the provider started employment, in YYYY-MM-DD format.
- employment_end_date: TEXT, NULL. Date the provider stopped working at the hospital, in YYYY-MM-DD format. Null if the provider is still employed. 
- created_at: TEXT, NOT NULL. UTC timestamp when the provider record was created, in YYYY-MM-DDTHH:MM:SSZ format.

## Appointments

- appointment_id: INTEGER, PRIMARY KEY, NOT NULL. Unique identifier for each appointment. 
- patient_id: INTEGER, NOT NULL, FOREIGN KEY. References Patients(patient_id). Identifies the patient who booked the appointment. 
- department_id: INTEGER, NOT NULL, FOREIGN KEY. References Departments(department_id). Identifies the department where the appointment is scheduled. 
- scheduled_at: TEXT, NOT NULL. UTC date and time when the appointment is scheduled to take place, in YYYY-MM-DDTHH:MM:SSZ format.
- status: TEXT, NOT NULL. Current appointment status: completed, cancelled, or no_show. 
- cancelled_at: TEXT, NULL. UTC timestamp when the appointment was cancelled, in YYYY-MM-DDTHH:MM:SSZ format. NULL if the appointment was not cancelled.
- created_at: TEXT, NOT NULL. UTC timestamp when the appointment record was created, in YYYY-MM-DDTHH:MM:SSZ format.

## Visits

- visit_id: INTEGER, PRIMARY KEY, NOT NULL. Unique identifier for each patient visit. 
- patient_id: INTEGER, NOT NULL, FOREIGN KEY. References Patients(patient_id). Identifies the patient associated with the visit. 
- department_id: INTEGER, NOT NULL, FOREIGN KEY. References Departments(department_id). Identifies the department where the patient visit occurred.
- provider_id: INTEGER, NULL, FOREIGN KEY. References Providers(provider_id). Identifies the provider who saw the patient. NULL if the patient left without being seen.  
- appointment_id: INTEGER, NULL, FOREIGN KEY. References Appointments(appointment_id). Identifies the appointment linked to this visit. NULL for emergency and walk-in visits. 
- visit_type: TEXT, NOT NULL. Type of patient visit: scheduled_outpatient, emergency, or walk_in_outpatient.
- arrival_at: TEXT, NOT NULL. UTC timestamp when the patient arrived at the hospital, in YYYY-MM-DDTHH:MM:SSZ format.  
- provider_seen_at: TEXT, NULL. UTC timestamp when the provider first saw the patient, in YYYY-MM-DDTHH:MM:SSZ format. NULL if the patient left without being seen. 
- discharge_at: TEXT, NOT NULL. UTC timestamp when the patient left the hospital, in YYYY-MM-DDTHH:MM:SSZ format.
- arrival_local_date: TEXT, NOT NULL. Date of the patient's arrival in the hospital's local time zone (America/Chicago), in YYYY-MM-DD format. 
- disposition: TEXT, NOT NULL. Outcome of the patient visit: discharged, admitted, transferred, or left_without_being_seen.
- mental_health_flag: INTEGER, NOT NULL. Indicates whether the visit involves a mental health concern (0 = No, 1 = yes).
- created_at: TEXT, NOT NULL. UTC timestamp when the visit record was created, in YYYY-MM-DDTHH:MM:SSZ format.

## Billing

- billing_id: INTEGER, PRIMARY KEY, NOT NULL. Unique identifier for each billing record.
- visit_id: INTEGER, NOT NULL, UNIQUE, FOREIGN KEY. References Visits(visit_id). Identifies the patient visit associated with this billing record.
- recorded_total_cents: INTEGER, NOT NULL. Total amount billed for the visit, stored in cents.
- billing_status: TEXT, NOT NULL. Current status of the billing record: Pending, Paid, or Denied.
- created_at: TEXT, NOT NULL. UTC timestamp when the billing record was created, in YYYY-MM-DDTHH:MM:SSZ format. 

## ChargeItems 

- charge_item_id: INTEGER, PRIMARY KEY, NOT NULL. Unique identifier for each charge item.
- billing_id: INTEGER, NOT NULL, FOREIGN KEY. References Billing (billing_id). Identifies the billing record this charge item belongs to. 
- charge_code: TEXT, NOT NULL. Code identifying the service or item being billed. 
- description: TEXT, NOT NULL. Description of the service or item being charged. 
- quantity: INTEGER, NOT NULL. Number of units billed for this charge item. 
- unit_amount_cents: INTEGER, NOT NULL. Price per unit for this charge item, stored in cents. 
- created_at: TEXT, NOT NULL. UTC timestamp when the charge item record was created, in YYYY-MM-DDTHH:MM:SSZ format.

## Raw Staging 

- source_row_id: INTEGER, NOT NULL. Identifies an incoming raw record within a pipeline run. Part of the composite primary key (pipeline_run_id, source_row_id).
- pipeline_run_id: INTEGER, NOT NULL, FOREIGN KEY. References PipelineRuns (pipeline_run_id). Identifies the pipeline execution that loaded this raw record. 
- source_order: INTEGER, NOT NULL. Original position of the record in the incoming dataset, used to determine which duplicate record to keep.  

Raw staging tables preserve incoming data before validation. They allow NULL values and duplicate business IDs so data quality errors can be detected and quarantined. Each raw staging table contains all business columns from its corresponding clean table, using the same column names. Every business column is stored as nullable TEXT. Raw staging tables have no foreign keys to other staging tables. The derived arrival_local_date column is excluded from raw staging and calculated in python during the clean load, after validation.

## ValidationResults

- validation_result_id: INTEGER, PRIMARY KEY, NOT NULL. Unique identifier for each validation result.
- pipeline_run_id: INTEGER, NOT NULL, FOREIGN KEY. References PipelineRuns (pipeline_run_id). Identifies the pipeline execution that produced this validation result. 
- rule_id: TEXT, NOT NULL. Identifier of the data quality rule that was checked.
- table_name: TEXT, NOT NULL. Name of the source table where the data quality rule was checked. 
- source_row_id: INTEGER, NULL. Identifies the raw staging record associated with this validation result. NULL if the result applies to the entire table.
- status: TEXT, NOT NULL. Validation outcome: Failed, Flagged, Skipped, or Passed. 
- error_message: TEXT, NULL. Description of the data quality problem found. NULL if the validation passed or was skipped.
- checked_at: TEXT, NOT NULL. UTC timestamp when the validation check was performed, in YYYY-MM-DDTHH:MM:SSZ format.
- affected_count: INTEGER, NOT NULL. Number of records affected by this validation result.

## QuarantineRecords

- quarantine_id: INTEGER, PRIMARY KEY, NOT NULL. Unique identifier for each quarantined record.
- pipeline_run_id: INTEGER, NOT NULL, FOREIGN KEY. References PipelineRuns (pipeline_run_id). Identifies the pipeline execution that quarantined this record. 
- table_name: TEXT, NOT NULL. Name of the source table containing the quarantined record. 
- source_row_id: INTEGER, NOT NULL. Identifies the original raw staging record that was quarantined. Together, pipeline_run_id, table_name, and source_row_id form a UNIQUE constraint, so each raw record can be quarantined only once per run. 
- rule_id: TEXT, NULL. Identifies the data quality rule that caused the record to be quarantined. NULL for dependency rejections that have no direct validation rule.  
- rejection_reason: TEXT, NOT NULL. Explains why the record was quarantined. When rule_id is NULL, rejection_reason must contain the code DEPENDENCY_REJECTED. 
- quarantined_at: TEXT, NOT NULL. UTC timestamp when the record was quarantined, in YYYY-MM-DDTHH:MM:SSZ format.

## PipelineRuns

- pipeline_run_id: INTEGER, PRIMARY KEY, NOT NULL. Unique identifier for each pipeline execution.
- started_at: TEXT, NOT NULL. UTC timestamp when the pipeline execution started, in YYYY-MM-DDTHH:MM:SSZ format.
- completed_at: TEXT, NULL. UTC timestamp when the pipeline execution finished, in YYYY-MM-DDTHH:MM:SSZ format. NULL if the pipeline is still running.
- status: TEXT, NOT NULL. Current pipeline execution status: Running, Completed, or Failed.
- total_records: INTEGER, NOT NULL. Total number of raw records processed during this pipeline execution.  
- clean_records: INTEGER, NOT NULL. Number of records that passed validation and were loaded into the clean tables. 
- quarantined_records: INTEGER, NOT NULL. Number of distinct raw records rejected during validation, including dependency rejections. Each rejected record is counted once.
- error_message: TEXT, NULL. Description of the pipeline failure. NULL if the pipeline completed successfully or is still running. 
- config_version: TEXT, NOT NULL. Version of the configuration used for this pipeline run.
- random_seed: INTEGER, NOT NULL. Seed used to generate reproducible synthetic data for this pipeline run. 
- output_hash: TEXT, NULL. SHA-256 hash of the pipeline output, used to verify that gnerated results have not changed.

## PipelineTableCounts

- pipeline_run_id: INTEGER, NOT NULL, FOREIGN KEY. References PipelineRuns (pipeline_run_id). Identifies the pipeline execution these counts belong to.
- table_name: TEXT, NOT NULL. Name of the source table whose record counts are being tracked. Together, pipeline_run_id and table_name form the composite primary key.
- raw_rows: INTEGER, NOT NULL. Total number of raw staging records received for this table during the pipeline run.
- accepted_rows: INTEGER, NOT NULL. Number of raw records that passed validation and were loaded into the clean table. 
- quarantined_rows: INTEGER, NOT NULL. Number of distinct raw records rejected from this table during the pipeline run, including dependency rejections. Each rejected record is counted once.
- dependency_rejected_rows: INTEGER, NOT NULL. Number of quarantined records rejected because they depend on another record that failed validation. This count is included in quarantined_rows. 
- flagged_rows: INTEGER, NOT NULL. Number of distinct raw records flagged for data quality concerns without being rejected. Each flagged record is counted once.  

## InjectionManifest

- injection_id: INTEGER, PRIMARY KEY, NOT NULL. Unique identifier for each intentionally injected data quality error. 
- pipeline_run_id: INTEGER, NOT NULL. Identifies the pipeline run associated with this injected error. Stored as a plain integer refernce, without a foreign key, because InjectionManifest is maintained separately from the pipeline database. 
- table_name: TEXT, NOT NULL. Name of the raw staging table where the error was intentionally injected.
- source_row_id: INTEGER, NOT NULL. Identifies the raw staging record where the error was intentionally injected. Assigned when the raw copy is created, so the same ID appears in both InjectionManifest and raw staging. 
- rule_id: TEXT, NOT NULL. Identifies the data quality rule associated with the intentionally injected error. 
- error_type: TEXT, NOT NULL. Describes the type of data quality error intentionally introduced into the raw staging record.
- original_value: TEXT, NULL. Stores the value before the intentional error was introduced.
- injected_value: TEXT, NULL. Stores the modified value after the intentional error was introduced. 
- injected_at: TEXT, NOT NULL. UTC timestamp when the intentional error was introduced, in YYYY-MM-DDTHH:MM:SSZ format. 

InjectionManifest is stored in a separate file or database that the validator connot access. For the first slice, expected error counts per rule are calculated by grouping InjectionManifest records by rule_id. A dedicated expected counts structure will be added in Slice 3F to account for dependency rejections. 