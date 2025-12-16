prompts = {
    "create_separate_modulefiles": {
        "system": """You are an expert Verilog code parser. Your task is to extract individual Verilog modules from a given text and output them in a JSON object. 
                    Each JSON key must be the module name, and each value must be the full module code including `module` and `endmodule` and all the dependent modules and also if any specific instructions provided as comment for that module to evalute include that too in the code as a commented section.
                    Your response must contain only valid JSON and no explanations or markdown formatting.
                    If no modules are found, return an empty JSON object {}.""", 

        "content": """Extract all Verilog modules from the following text and return them in JSON format.

                        Requirements:
                        - Identify modules starting with `module <name>` and ending with `endmodule`
                        - Use the module name as the JSON key
                        - Include the full code for each module as the value
                        - If particular module is not found return value empty string for that module
                        - Output only raw JSON

                        Here are the module names to be detected and used as keys if that module is not present set the value to empty string for that
                        ((modules))

                        Here is the input code:
                        ((code))
                        """
    },

    "evaluate_module": {
        "system": """You are an expert in verilog. Your task is to generate a test bench for the verilog modules and grade them accoding to you. You will get full question, the module to be evaluated, answer code for that module, student code for that module, you have to return a valid JSON object that will have a key code wihich will have student code for that module and test bench that you generate and one more key would be marks that will be marks for this module.
        Your response must contain only valid JSON and no explanations or markdown formatting.""",

        "content": """.

                        Requirements:
                        - Create the test bench for the student code on the inputs should be like student and the logic should be according to answer code provided
                        - The JSON should have keys code(student module and test bench) and marks(probable marks accroding to you float)
                        - Output only raw JSON

                        Question:
                        ((question))

                        The module to be evaluated:
                        ((module)) - (marks: ((marks)))

                        Here is the a answer code:
                        ((answercode))

                        Here is the student code:
                        ((studentcode))
                        """

    }
}