import os
import json
import Models.gemini as gemini
import prompt_template
import utils
import run_v
import shutil


def create_question_with_separate_modulefiles(answer_scheme, modules, question_name, question_txt):

    os.makedirs(f"QuestionBank/{question_name}", exist_ok=True)
    with open(f"QuestionBank/{question_name}/question.txt", "w") as f:
        f.write(question_txt)
    with open(f"QuestionBank/{question_name}/answer_scheme.v", "w") as f:
        f.write(answer_scheme)
    with open(f"QuestionBank/{question_name}/modules.csv", "w") as f:
        for mod, marks in modules:
            f.write(f"{mod},{marks}\n")

    # Build comma separated module names string
    module_names = ", ".join(mod for mod, key in modules)

    prompt = {}
    prompt["system"] = prompt_template.prompts["create_separate_modulefiles"]["system"]
    prompt["content"] = prompt_template.prompts["create_separate_modulefiles"]["content"]

    # Use replace correctly & assign updated value
    prompt["content"] = prompt["content"].replace("((modules))", module_names)
    prompt["content"] = prompt["content"].replace("((code))", answer_scheme)

    try:
        # Gemini call returns JSON string
        module_codes_json = gemini.generate(prompt)

        try:
            module_codes = utils.clean_json_output(module_codes_json)
        except Exception:
            module_codes = json.loads(module_codes_json)

        # Create output directory
        base_path = f"QuestionBank/{question_name}/module_codes"
        os.makedirs(base_path, exist_ok=True)

        # Write each module into its own .v file
        for module_name, module_code in module_codes.items():
            file_path = os.path.join(base_path, f"{module_name}.v")
            with open(file_path, "w") as f:
                f.write(module_code)

        print("Module files generated successfully.")

    except Exception as e:
        print("Error:", e)



def main(question, solutions, selected_modules, progress_callback=None):
    try:
        # Paths
        question_path = f"QuestionBank/{question}/question.txt"
        answer_scheme_path = f"QuestionBank/{question}/answer_scheme.v"
        student_solutions_folder_path = f"SolutionBank/{solutions}"
        module_codes_folder_path = f"QuestionBank/{question}/module_codes/"

        # Results folder
        result_folder = os.path.join("Results", f"{question}-{solutions}")
        os.makedirs(result_folder, exist_ok=True)

        # Read modules & supporting files
        modules = utils.read_module_csv(f"QuestionBank/{question}/modules.csv")
        question_txt = utils.read_txt_file(question_path)
        answer_scheme = utils.read_txt_file(answer_scheme_path)

        student_files = [
            f for f in os.listdir(student_solutions_folder_path)
            if os.path.isfile(os.path.join(student_solutions_folder_path, f))
        ]
        total_students = len(student_files)

        # Process each student
        for idx, filename in enumerate(student_files, start=1):
            report_path = None
            try:
                if progress_callback:
                    progress_callback(idx, total_students)

                filepath = os.path.join(student_solutions_folder_path, filename)

                # Extract student ID
                base_name = os.path.splitext(filename)[0]
                student_id = base_name.split('_')[-1].split('.')[0]

                # Student results directory
                student_result_dir = os.path.join(result_folder, student_id)
                os.makedirs(student_result_dir, exist_ok=True)

                # Copy full module file
                all_modules_path = os.path.join(student_result_dir, "all_modules.v")
                shutil.copy(filepath, all_modules_path)

                # Run complete code (safe)
                try:
                    compilation_and_execution_output = run_v.compile_and_run(all_modules_path)
                except Exception as e:
                    compilation_and_execution_output = f"[ERROR running full file: {e}]"

                # Create report
                report_path = os.path.join(student_result_dir, "report.txt")
                with open(report_path, "w") as report_f:
                    report_f.write("=== Full File Compilation and Execution Logs ===\n\n")
                    report_f.write(str(compilation_and_execution_output))
                    report_f.write("\n")

                student_full_solution = utils.read_txt_file(all_modules_path)

                # use selected_modules list for the prompt
                module_names = ", ".join(selected_modules)

                prompt = {}
                prompt["system"] = prompt_template.prompts["create_separate_modulefiles"]["system"]
                prompt["content"] = prompt_template.prompts["create_separate_modulefiles"]["content"]

                prompt["content"] = prompt["content"].replace("((modules))", module_names)
                prompt["content"] = prompt["content"].replace("((code))", student_full_solution)

                student_modulewise_code_json = gemini.generate(prompt)
                try:
                    student_modulewise_code = utils.clean_json_output(student_modulewise_code_json)
                except Exception:
                    student_modulewise_code = json.loads(student_modulewise_code_json)

                # --- Per-module loop over selected_modules ---
                for module_name in selected_modules:
                    try:
                        module_ref_path = os.path.join(module_codes_folder_path, f"{module_name}.v")
                        reference_module_code = utils.read_txt_file(module_ref_path)
                        student_module_code = student_modulewise_code[module_name]
                        module_marks = modules[module_name]

                        prompt = {}
                        prompt["system"] = prompt_template.prompts["evaluate_module"]["system"]
                        prompt["content"] = prompt_template.prompts["evaluate_module"]["content"]

                        prompt["content"] = prompt["content"].replace("((question))", question_txt)
                        prompt["content"] = prompt["content"].replace("((module))", module_name)
                        prompt["content"] = prompt["content"].replace("((marks))", str(module_marks))
                        prompt["content"] = prompt["content"].replace("((answercode))", reference_module_code)
                        prompt["content"] = prompt["content"].replace("((studentcode))", student_module_code)

                        module_evaluation_json = gemini.generate(prompt)
                        try:
                            module_evaluation = utils.clean_json_output(module_evaluation_json)
                        except Exception:
                            module_evaluation = json.loads(module_evaluation_json)

                        evaluated_code = module_evaluation["code"]
                        evaluated_marks = module_evaluation["marks"]

                        module_file_path = os.path.join(student_result_dir, f"{module_name}.v")
                        with open(module_file_path, "w") as mf:
                            mf.write(evaluated_code)

                        # SAFE run
                        try:
                            module_run_logs = run_v.compile_and_run(module_file_path)
                        except Exception as e:
                            module_run_logs = f"[ERROR running {module_name}: {e}]"

                        with open(report_path, "a") as report_f:
                            report_f.write("\n")
                            report_f.write(f"=== {module_name} ===\n\n")
                            report_f.write(str(module_run_logs))
                            report_f.write("\n")
                            report_f.write(f"\nProbable marks: {evaluated_marks}/{module_marks}\n")

                    except Exception as e:
                        # Per-module error log, but keep going with next module
                        if report_path:
                            with open(report_path, "a") as report_f:
                                report_f.write(f"\n[ERROR] Module {module_name} failed: {str(e)}\n")
                        else:
                            print(f"[ERROR] Module {module_name} failed for student {filename}: {e}")
                        continue  # next module

            except Exception as e:
                # Student-level failure: move to next student
                print(f"[ERROR] Failed processing student {filename}: {e}")
                if report_path:
                    with open(report_path, "a") as report_f:
                        report_f.write(f"\n[ERROR] Failed processing student: {str(e)}\n")
                continue  # next student

        print("All evaluations completed successfully.")

    except Exception as e:
        print(f"[CRITICAL ERROR] Failed running main evaluation: {e}")


